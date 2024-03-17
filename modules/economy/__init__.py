import asyncio
import logging
import random

import discord
from discord.ext import commands, bridge

from handlers.ItemHandler import ItemHandler
from lib import economy_embeds, economy_functions, checks, interaction, embeds, err_embeds
from main import economy_config, strings
from modules.economy import leaderboard, blackjack, sell, slots, balance
from services.BlackJackStats import BlackJackStats
from services.Currency import Currency
from services.Inventory import Inventory
from services.Item import Item
from services.SlotsStats import SlotsStats
from services.Xp import Xp

logs = logging.getLogger('Racu.Core')
active_blackjack_games = {}


class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client

    @bridge.bridge_command(
        name="leaderboard",
        aliases=["lb", "xplb"],
        description="Are ya winning' son?",
        help="Shows the guild's level leaderboard by default. You can switch to currency and /daily leaderboard.",
        guild_only=True
    )
    @commands.check(checks.channel)
    @commands.cooldown(1, 180, commands.BucketType.user)
    async def leaderboard_command(self, ctx):
        await leaderboard.cmd(ctx)

    @bridge.bridge_command(
        name="balance",
        aliases=["bal", "$"],
        description="See how much cash you have.",
        help="Shows your current Racu balance. The economy system is global, meaning your balance will be the same in "
             "all servers.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def balance_command(self, ctx):
        await balance.cmd(ctx)

    @bridge.bridge_command(
        name="blackjack",
        aliases=["bj"],
        description="Start a game of blackjack.",
        help="Start a game of blackjack.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def blackjack_command(self, ctx, *, bet: int):

        """
        status states:
        0 = game start
        1 = player busted
        2 = player won with 21 (after hit)
        3 = dealer busted
        4 = dealer won
        5 = player won with 21 (blackjack)
        6 = timed out
        """

        # check if the player already has an active blackjack going
        if ctx.author.id in active_blackjack_games:
            await ctx.respond(embed=economy_embeds.already_playing("BlackJack"))
            return

        # Currency handler
        ctx_currency = Currency(ctx.author.id)

        # check if the user has enough cash
        player_balance = ctx_currency.balance
        if bet > player_balance:
            return await ctx.respond(embed=err_embeds.InsufficientBalance(ctx))
        elif bet <= 0:
            return await ctx.respond(embed=err_embeds.BadBetArgument(ctx))

        # check if the bet exceeds the bet limit
        # bet_limit = int(economy_config["bet_limit"])
        # if abs(bet) > bet_limit:
        #     message = strings["bet_limit"].format(ctx.author.name, Currency.format_human(bet_limit))
        #     return await ctx.respond(content=message)

        active_blackjack_games[ctx.author.id] = True

        try:

            player_hand = []
            dealer_hand = []
            deck = economy_functions.blackjack_get_new_deck()
            multiplier = float(economy_config["blackjack"]["reward_multiplier"])

            # deal initial cards (player draws two & dealer one)
            player_hand.append(economy_functions.blackjack_deal_card(deck))
            player_hand.append(economy_functions.blackjack_deal_card(deck))
            dealer_hand.append(economy_functions.blackjack_deal_card(deck))

            # calculate initial hands
            player_hand_value = economy_functions.blackjack_calculate_hand_value(player_hand)
            dealer_hand_value = economy_functions.blackjack_calculate_hand_value(dealer_hand)

            status = 0 if player_hand_value != 21 else 5
            view = interaction.BlackJackButtons(ctx)
            playing_embed = False

            while status == 0:
                if not playing_embed:
                    await ctx.respond(embed=blackjack.blackjack_show(ctx, Currency.format_human(bet), player_hand,
                                                                     dealer_hand, player_hand_value,
                                                                     dealer_hand_value),
                                      view=view,
                                      content=ctx.author.mention)

                    playing_embed = True

                await view.wait()

                if view.clickedHit:
                    # player draws a card & value is calculated
                    player_hand.append(economy_functions.blackjack_deal_card(deck))
                    player_hand_value = economy_functions.blackjack_calculate_hand_value(player_hand)

                    if player_hand_value > 21:
                        status = 1
                        break
                    elif player_hand_value == 21:
                        status = 2
                        break

                elif view.clickedStand:
                    # player stands, dealer draws cards until he wins OR busts
                    while dealer_hand_value <= player_hand_value:
                        dealer_hand.append(economy_functions.blackjack_deal_card(deck))
                        dealer_hand_value = economy_functions.blackjack_calculate_hand_value(dealer_hand)

                    if dealer_hand_value > 21:
                        status = 3
                        break
                    else:
                        status = 4
                        break

                else:
                    status = 6
                    break

                # refresh
                view = interaction.BlackJackButtons(ctx)
                embed = blackjack.blackjack_show(ctx, Currency.format_human(bet), player_hand,
                                                 dealer_hand, player_hand_value,
                                                 dealer_hand_value)

                await ctx.edit(embed=embed, view=view, content=ctx.author.mention)

            """
            At this point the game has concluded, generate a final output & backend
            """
            payout = bet * multiplier if not status == 5 else bet * 2
            is_won = False if status == 1 or status == 4 else True

            embed = blackjack.blackjack_finished(ctx, Currency.format_human(bet), player_hand_value,
                                                 dealer_hand_value, Currency.format_human(payout), status)

            item_reward = ItemHandler(ctx)
            field = await item_reward.rave_coin(is_won=is_won, bet=bet, field="")
            field = await item_reward.bitch_coin(status, field)

            if field is not "":
                embed.add_field(name="Extra Rewards", value=field, inline=False)

            if playing_embed:
                await ctx.edit(embed=embed, view=None, content=ctx.author.mention)
            else:
                await ctx.respond(embed=embed, view=None, content=ctx.author.mention)

            # change balance
            # if status == 1 or status == 4:
            if not is_won:
                ctx_currency.take_balance(bet)
                ctx_currency.push()

                # push stats (low priority)
                stats = BlackJackStats(
                    user_id=ctx.author.id,
                    is_won=False,
                    bet=bet,
                    payout=0,
                    hand_player=player_hand,
                    hand_dealer=dealer_hand
                )
                stats.push()

            elif status == 6:
                await ctx.send(embed=economy_embeds.out_of_time(), content=ctx.author.mention)
                ctx_currency.take_balance(bet)
                ctx_currency.push()

            else:
                ctx_currency.add_balance(payout)
                ctx_currency.push()

                # push stats (low priority)
                stats = BlackJackStats(
                    user_id=ctx.author.id,
                    is_won=True,
                    bet=bet,
                    payout=payout,
                    hand_player=player_hand,
                    hand_dealer=dealer_hand
                )
                stats.push()

        except Exception as e:
            await ctx.respond(embed=embeds.command_error_1(e))
            logs.error("[CommandHandler] Something went wrong in the gambling command: ", e)

        finally:
            # remove player from active games list
            del active_blackjack_games[ctx.author.id]

    @blackjack_command.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.respond(embed=err_embeds.MissingBet(ctx))
        elif isinstance(error, commands.BadArgument):
            await ctx.respond(embed=err_embeds.BadBetArgument(ctx))
        else:
            raise error

    @bridge.bridge_command(
        name="give",
        description="Give another user some currency.",
        help="Give another server member some cash.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def give(self, ctx, *, user: discord.Member, amount: int):

        if ctx.author.id == user.id:
            embed = discord.Embed(
                color=discord.Color.red(),
                description=f"You can't give money to yourself, silly."
            )
            return await ctx.respond(embed=embed)
        elif user.bot:
            embed = discord.Embed(
                color=discord.Color.red(),
                description=f"You can't give money to a bot, silly."
            )
            return await ctx.respond(embed=embed)

        # Currency handler
        ctx_currency = Currency(ctx.author.id)
        target_currency = Currency(user.id)

        try:
            author_balance = ctx_currency.balance

            if author_balance < amount or author_balance <= 0:
                return await ctx.respond(embed=economy_embeds.not_enough_cash())

            target_currency.add_balance(amount)
            ctx_currency.take_balance(amount)

            ctx_currency.push()
            target_currency.push()

        except Exception as e:
            await ctx.respond("Something funky happened.. Sorry about that.", ephemeral=True)
            print(e)
            return

        embed = discord.Embed(
            color=discord.Color.green(),
            description=f"**{ctx.author.name}** gave **${Currency.format(amount)}** to {user.name}."
        )
        embed.set_footer(text="Say thanks! :)")

        await ctx.respond(embed=embed)

    @bridge.bridge_command(
        name="inventory",
        aliases=["inv"],
        description="Display your inventory.",
        help="Display your inventory, this will also show your Racu badges if you have any.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def inventory(self, ctx):
        inventory = Inventory(ctx.author.id)
        inventory_dict = inventory.get_inventory()

        description = "You don't have any items!" if inventory_dict == {} else None

        embed = discord.Embed(
            color=discord.Color.embed_background(),
            description=description
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)

        for item, quantity in inventory_dict.items():
            if item.type == "badge":

                if not embed.description:
                    embed.description = "**Badges:** "

                emote = self.client.get_emoji(item.emote_id)
                embed.description += f"{emote} "

            else:
                emote = self.client.get_emoji(item.emote_id)
                embed.add_field(name=f"{emote} {item.display_name.capitalize()}",
                                value=f"*— amount: `{quantity}`*",
                                inline=False)

        await ctx.respond(embed=embed)

    @commands.slash_command(
        name="sell",
        description="Sell items from your inventory.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def sell_command(self, ctx):
        inv = Inventory(ctx.author.id)
        items = inv.get_sell_data()

        def response_check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        if not items:
            embed = discord.Embed(
                color=discord.Color.red(),
                description="You don't have any items to sell."
            )
            return await ctx.respond(embed=embed)

        options = sell.SellCommandOptions(items)
        view = sell.SellCommandView(ctx, options)

        embed = discord.Embed(
            color=discord.Color.embed_background(),
            description="Please select the item you want to sell."
        )
        await ctx.respond(embed=embed, view=view, content=ctx.author.mention)

        await view.wait()
        item = view.item

        if item:
            item = Item.get_item_by_display_name(view.item)
            quantity = item.get_quantity(ctx.author.id)

            if quantity == 1:
                embed = discord.Embed(
                    color=discord.Color.embed_background(),
                    description=f"You selected **{item.display_name}**, you have this item only once."
                )
                await ctx.edit(embed=embed)
                amount_to_sell = 1

            elif quantity > 1:
                embed = discord.Embed(
                    color=discord.Color.embed_background(),
                    description=f"You selected **{item.display_name}**, you have this item **{quantity}** times.\n"
                )
                embed.set_footer(text=f"Please type the amount you want to sell in this chat.")
                await ctx.edit(embed=embed)

                try:
                    amount_message = await self.client.wait_for('message', check=response_check, timeout=60)
                    amount = amount_message.content

                    if sell.is_number_between(amount, quantity):
                        amount_to_sell = int(amount)

                    else:
                        embed = discord.Embed(
                            color=discord.Color.red(),
                            description="Invalid input... try the command again."
                        )
                        return await ctx.respond(embed=embed, content=ctx.author.mention)

                except asyncio.TimeoutError:
                    await ctx.respond(
                        embed=discord.Embed(description="You ran out of time.", color=discord.Color.red()),
                        content=ctx.author.mention)
                    # logs.warning(f"{ctx.author.id} Sell Timeout")
                    return

            else:
                embed = discord.Embed(
                    color=discord.Color.red(),
                    description="You dont have this item."
                )
                embed.set_footer(text="It shouldn't have showed up in the list, my apologies.")
                return await ctx.edit(embed=embed)

            """
            Item & amount selection finished.
            Get price, confirmation message & handle balances.
            """
            currency = Currency(ctx.author.id)
            worth = item.get_item_worth()
            total = worth * amount_to_sell
            view = interaction.ExchangeConfirmation(ctx)
            embed = discord.Embed(
                color=discord.Color.embed_background(),
                description=f"You're about to sell **{amount_to_sell} {item.display_name}(s)** for **${total}**. "
                            f"Are you absolutely sure about this?"
            )
            message = await ctx.respond(embed=embed, view=view, content=ctx.author.mention)
            await view.wait()

            if view.clickedConfirm:

                try:
                    currency.balance += total
                    currency.push()
                    inv.take_item(item, amount_to_sell)

                    embed = discord.Embed(
                        color=discord.Color.green(),
                        description=f"You have successfully sold "
                                    f"**{amount_to_sell} {item.display_name}(s)** for **${total}**."
                    )
                    await message.edit(embed=embed, view=None)

                except Exception as e:
                    await ctx.respond("Something went wrong.")
                    logs.error(f"[CommandHandler] /sell post-confirmation error: {e}")
                    return

            else:
                return await message.edit(embed=None, content=f"**{ctx.author.name}** canceled the command.")

        else:
            embed = discord.Embed(
                color=discord.Color.red(),
                description="You selected not to sell anything."
            )
            await ctx.edit(embed=embed)

    @bridge.bridge_command(
        name="slots",
        aliases=["slot"],
        descriptions="Spin the slots for a chance to win the jackpot!",
        help="Starts a slots game.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def slots_command(self, ctx, *, bet: int):

        # Currency handler
        ctx_currency = Currency(ctx.author.id)

        # check if the user has enough cash
        player_balance = ctx_currency.balance
        if bet > player_balance:
            return await ctx.respond(embed=err_embeds.InsufficientBalance(ctx))
        elif bet <= 0:
            return await ctx.respond(embed=err_embeds.BadBetArgument(ctx))

        # # check if the bet exceeds the bet limit
        # bet_limit = int(economy_config["bet_limit"])
        # if abs(bet) > bet_limit:
        #     message = strings["bet_limit"].format(ctx.author.name, Currency.format_human(bet_limit))
        #     return await ctx.respond(content=message)

        # calculate the results before the command is shown
        results = [random.randint(0, 6) for _ in range(3)]
        calculated_results = slots.calculate_slots_results(bet, results)

        (type, payout, multiplier) = calculated_results
        is_won = True

        if type == "lost":
            is_won = False

        # only get the emojis once
        emojis = slots.get_emotes(self.client)

        # start with default "spinning" embed
        await ctx.respond(embed=slots.slots_spinning(ctx, 3, Currency.format_human(bet), results, emojis))
        await asyncio.sleep(1)

        for i in range(2, 0, -1):
            await ctx.edit(embed=slots.slots_spinning(ctx, i, Currency.format_human(bet), results, emojis))
            await asyncio.sleep(1)

        # output final result
        finished_output = slots.slots_finished(ctx, type, Currency.format_human(bet),
                                               Currency.format_human(payout), results, emojis)

        item_reward = ItemHandler(ctx)
        field = await item_reward.rave_coin(is_won=is_won, bet=bet, field="")

        if field is not "":
            finished_output.add_field(name="Extra Rewards", value=field, inline=False)

        await ctx.edit(embed=finished_output)

        # user payout
        if payout > 0:
            ctx_currency.add_balance(payout)
        else:
            ctx_currency.take_balance(bet)

        # item_reward = ItemHandler(ctx)
        # await item_reward.rave_coin(is_won=is_won, bet=bet)

        stats = SlotsStats(
            user_id=ctx.author.id,
            is_won=is_won,
            bet=bet,
            payout=payout,
            spin_type=type,
            icons=results
        )

        ctx_currency.push()
        stats.push()

    @slots_command.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.respond(embed=err_embeds.MissingBet(ctx))
        elif isinstance(error, commands.BadArgument):
            await ctx.respond(embed=err_embeds.BadBetArgument(ctx))
        else:
            raise error

    @commands.slash_command(
        name="stats",
        description="Display your stats (BETA)",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def stats(self, ctx, *, game: discord.Option(choices=["BlackJack", "Slots"])):
        output = ""

        if game == "BlackJack":
            stats = BlackJackStats.get_user_stats(ctx.author.id)

            # amount formatting
            total_bet = Currency.format_human(stats["total_bet"])
            total_payout = Currency.format_human(stats["total_payout"])

            # output = f"{ctx.author.name}'s racu stats\n\n"
            output = strings["stats_blackjack"].format(
                stats["amount_of_games"],
                total_bet,
                stats["winning_amount"],
                total_payout
            )

        elif game == "Slots":
            stats = SlotsStats.get_user_stats(ctx.author.id)

            # amount formatting
            total_bet = Currency.format_human(stats["total_bet"])
            total_payout = Currency.format_human(stats["total_payout"])

            output = strings["stats_slots"].format(stats["amount_of_games"], total_bet, total_payout)
            output += "\n\n"

            pair_emote = self.client.get_emoji(economy_config["slots"]["emotes"]["slots_0_id"])
            three_emote = self.client.get_emoji(economy_config["slots"]["emotes"]["slots_4_id"])
            diamonds_emote = self.client.get_emoji(economy_config["slots"]["emotes"]["slots_5_id"])
            seven_emote = self.client.get_emoji(economy_config["slots"]["emotes"]["slots_6_id"])

            output += f"{pair_emote} | **{stats['games_won_pair']}** pairs.\n"
            output += f"{three_emote} | **{stats['games_won_three_of_a_kind']}** three-of-a-kinds.\n"
            output += f"{diamonds_emote} | **{stats['games_won_three_diamonds']}** triple diamonds.\n"
            output += f"{seven_emote} | **{stats['games_won_jackpot']}** jackpots."

        output += "\n\n *This command is still in beta, stats may be slightly inaccurate.*"
        await ctx.respond(content=output)


def setup(client):
    client.add_cog(Economy(client))
