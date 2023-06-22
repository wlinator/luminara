import asyncio
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

from data.BlackJackStats import BlackJackStats
from data.Currency import Currency
from data.SlotsStats import SlotsStats
from main import economy_config
from sb_tools import economy_embeds, economy_functions, universal, interaction, embeds

load_dotenv('.env')

active_blackjack_games = {}
special_balance_name = os.getenv("SPECIAL_BALANCE_NAME")
cash_balance_name = os.getenv("CASH_BALANCE_NAME")


class Gambling(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot

    @commands.slash_command(
        name="blackjack",
        description="Start a game of blackjack.",
        guild_only=True
    )
    @commands.check(universal.channel_check)
    async def blackjack(self, ctx, *, bet: discord.Option(int)):

        # check if the player already has an active blackjack going
        if ctx.author.id in active_blackjack_games:
            await ctx.respond(embed=economy_embeds.already_playing("BlackJack"))
            return

        # Currency handler
        ctx_currency = Currency(ctx.author.id)

        # check if the user has enough cash
        player_cash_balance = ctx_currency.cash
        if bet > player_cash_balance or bet <= 0:
            await ctx.respond(embed=economy_embeds.not_enough_cash())
            return

        active_blackjack_games[ctx.author.id] = True

        try:

            player_hand = []
            dealer_hand = []
            deck = economy_functions.blackjack_get_new_deck()
            view = interaction.BlackJackButtons(ctx)

            # deal initial cards (player draws two & dealer one)
            player_hand.append(economy_functions.blackjack_deal_card(deck))
            player_hand.append(economy_functions.blackjack_deal_card(deck))
            dealer_hand.append(economy_functions.blackjack_deal_card(deck))

            # calculate initial hands
            player_hand_value = economy_functions.blackjack_calculate_hand_value(player_hand)
            dealer_hand_value = economy_functions.blackjack_calculate_hand_value(dealer_hand)

            status = "game_start"

            await ctx.respond(embed=economy_embeds.blackjack_show(ctx, bet, player_hand,
                                                                  dealer_hand, player_hand_value,
                                                                  dealer_hand_value, status=status), view=view,
                              content=ctx.author.mention)

            while status == "game_start":
                await view.wait()

                if view.clickedHit:
                    # player draws a card & value is calculated
                    player_hand.append(economy_functions.blackjack_deal_card(deck))
                    player_hand_value = economy_functions.blackjack_calculate_hand_value(player_hand)

                    if player_hand_value > 21:
                        status = "player_busted"

                elif view.clickedStand:
                    # player stands, dealer draws cards until he wins OR busts
                    while dealer_hand_value <= player_hand_value:
                        dealer_hand.append(economy_functions.blackjack_deal_card(deck))
                        dealer_hand_value = economy_functions.blackjack_calculate_hand_value(dealer_hand)

                    if dealer_hand_value > 21:
                        status = "dealer_busted"
                    else:
                        status = "dealer_won"

                else:
                    status = "timed_out"
                    break

                # edit the embed, disable view if game is over.
                if status == "game_start":
                    view = interaction.BlackJackButtons(ctx)
                else:
                    view = None

                await ctx.edit(embed=economy_embeds.blackjack_show(ctx, bet, player_hand,
                                                                   dealer_hand, player_hand_value,
                                                                   dealer_hand_value, status=status), view=view,
                               content=ctx.author.mention)

            # change balance
            if status == "player_busted" or status == "dealer_won":
                ctx_currency.take_cash(bet)
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

            elif status == "timed_out":
                await ctx.send(embed=economy_embeds.out_of_time(), content=ctx.author.mention)
                ctx_currency.take_cash(bet)
                ctx_currency.push()

            else:
                # bet multiplier
                payout = bet * float(economy_config["blackjack"]["reward_multiplier"])
                ctx_currency.add_cash(payout)
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
            await ctx.respond(embed=embeds.command_error_1())
            print("Something went wrong in the gambling command:\n", e)

        finally:
            # remove player from active games list
            del active_blackjack_games[ctx.author.id]

    @commands.slash_command(
        name="slots",
        descriptions="Spin the slots for a chance to win the jackpot!",
        guild_only=True
    )
    @commands.check(universal.channel_check)
    async def slots(self, ctx, *, bet: discord.Option(int)):

        # Currency handler
        ctx_currency = Currency(ctx.author.id)

        # check if the user has enough cash
        player_cash_balance = ctx_currency.cash
        if bet > player_cash_balance or bet <= 0:
            await ctx.respond(embed=economy_embeds.not_enough_cash())
            return

        # calculate the results before the command is shown
        results = [random.randint(0, 6) for i in range(3)]
        calculated_results = economy_functions.calculate_slots_results(bet, results)

        type = calculated_results[0]
        payout = calculated_results[1]
        multiplier = calculated_results[2]
        is_won = True

        if type == "lost":
            is_won = False

        # start with default "spinning" embed
        await ctx.respond(embed=economy_embeds.slots_spinning(ctx, 3, bet, results, self.bot))
        await asyncio.sleep(1)
        await ctx.edit(embed=economy_embeds.slots_spinning(ctx, 2, bet, results, self.bot),
                       allowed_mentions=discord.AllowedMentions.none())
        await asyncio.sleep(1)
        await ctx.edit(embed=economy_embeds.slots_spinning(ctx, 1, bet, results, self.bot),
                       allowed_mentions=discord.AllowedMentions.none())
        await asyncio.sleep(1)
        await ctx.edit(embed=economy_embeds.slots_finished(ctx, type, multiplier, bet, results, self.bot),
                       allowed_mentions=discord.AllowedMentions.none())

        # user payout
        if payout >= 0:
            ctx_currency.add_cash(payout)
        else:
            ctx_currency.take_cash(payout)

        # push stats (low priority)
        if payout <= 0:
            payout = 0

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

    @commands.slash_command(
        name="duel",
        description="Challenge another player to a fight.",
        guild_only=True
    )
    @commands.check(universal.channel_check)
    async def duel(self, ctx, *, opponent: discord.Option(discord.Member), bet: discord.Option(int)):
        challenger = ctx.author

        if challenger.id == opponent.id:
            return await ctx.respond(content="You cannot duel yourself.")
        elif opponent.bot:
            return await ctx.respond(content="You cannot duel a bot.")

        # Currency handler
        challenger_currency = Currency(ctx.author.id)
        opponent_currency = Currency(opponent.id)

        # check if challenger has enough cash
        challenger_cash_balance = challenger_currency.cash
        if bet > challenger_cash_balance or bet <= 0:
            return await ctx.respond(embed=economy_embeds.not_enough_cash())

        # if opponent doesn't have sufficient money, the bet will become the opponent's cash
        opponent_cash_balance = opponent_currency.cash
        all_in = ""
        if opponent_cash_balance <= 0:
            return await ctx.respond(f"Woops, you can't do that because **{opponent.name}** has no money.")
        elif bet > opponent_cash_balance:
            bet = opponent_cash_balance
            all_in = " | opponent's all-in"

        # challenge message
        view = interaction.DuelChallenge(opponent)

        await ctx.respond(
            content=f"**{challenger.name}** challenges {opponent.mention} to a duel ({cash_balance_name}{bet}{all_in})\n"
                    f"Use the buttons to accept/deny (challenge expires after 60s)", view=view)
        await view.wait()

        if view.clickedConfirm:
            winner = random.choice([challenger, opponent])
            loser = opponent if winner == challenger else challenger
            combat_message = random.choice(economy_config["duel"]["combat_messages"]).format(f"**{winner.name}**",
                                                                                             f"**{loser.name}**")

            await ctx.respond(content=f"{combat_message}\n\n"
                                      f"{winner.mention} wins **{cash_balance_name}{bet}**\n"
                                      f"{loser.mention} loses this bet.")

            # payouts
            if winner == challenger:
                challenger_currency.add_cash(bet)
                opponent_currency.take_cash(bet)

            elif winner == opponent:
                opponent_currency.add_cash(bet)
                challenger_currency.take_cash(bet)

        elif view.clickedDeny:
            await ctx.edit(content=f"**{opponent.name}** canceled the duel.")

        else:
            await ctx.edit(content=f"Time ran out.")

        challenger_currency.push()
        opponent_currency.push()


def setup(sbbot):
    sbbot.add_cog(Gambling(sbbot))
