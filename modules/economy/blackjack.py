import logging
from datetime import datetime

import discord
import pytz
from dotenv import load_dotenv

from handlers.ItemHandler import ItemHandler
from lib import economy_embeds, economy_functions, interaction, embeds_old
from lib.embeds.error import EconErrors
from main import economy_config
from services.BlackJackStats import BlackJackStats
from services.Currency import Currency

logs = logging.getLogger('Racu.Core')
load_dotenv('.env')
est = pytz.timezone('US/Eastern')
active_blackjack_games = {}


async def cmd(ctx, bet: int):
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
        return await ctx.respond(embed=EconErrors.insufficient_balance(ctx))
    elif bet <= 0:
        return await ctx.respond(embed=EconErrors.bad_bet_argument(ctx))

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
                await ctx.respond(embed=blackjack_show(ctx, Currency.format_human(bet), player_hand,
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
            embed = blackjack_show(ctx, Currency.format_human(bet), player_hand,
                                   dealer_hand, player_hand_value,
                                   dealer_hand_value)

            await ctx.edit(embed=embed, view=view, content=ctx.author.mention)

        """
        At this point the game has concluded, generate a final output & backend
        """
        payout = bet * multiplier if not status == 5 else bet * 2
        is_won = False if status == 1 or status == 4 else True

        embed = blackjack_finished(ctx, Currency.format_human(bet), player_hand_value,
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
        await ctx.respond(embed=embeds_old.command_error_1(e))
        logs.error("[CommandHandler] Something went wrong in the gambling command: ", e)

    finally:
        # remove player from active games list
        del active_blackjack_games[ctx.author.id]


def blackjack_show(ctx, bet, player_hand, dealer_hand, player_hand_value, dealer_hand_value):
    current_time = datetime.now(est).strftime("%I:%M %p")
    thumbnail_url = None

    embed = discord.Embed(
        title="BlackJack",
        color=discord.Color.dark_orange()
    )

    embed.description = f"**You**\n" \
                        f"Score: {player_hand_value}\n" \
                        f"*Hand: {' + '.join(player_hand)}*\n\n"

    if len(dealer_hand) < 2:
        embed.description += f"**Dealer**\n" \
                             f"Score: {dealer_hand_value}\n" \
                             f"*Hand: {dealer_hand[0]} + ??*"
    else:
        embed.description += f"**Dealer | Score: {dealer_hand_value}**\n" \
                             f"*Hand: {' + '.join(dealer_hand)}*"

    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.set_footer(text=f"Bet ${bet} • deck shuffled • Today at {current_time}",
                     icon_url="https://i.imgur.com/96jPPXO.png")

    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)

    return embed


def blackjack_finished(ctx, bet, player_hand_value, dealer_hand_value, payout, status):
    current_time = datetime.now(est).strftime("%I:%M %p")
    thumbnail_url = None

    embed = discord.Embed(
        title="BlackJack"
    )
    embed.description = f"You | Score: {player_hand_value}\n" \
                        f"Dealer | Score: {dealer_hand_value}"
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.set_footer(text=f"Game finished • Today at {current_time}",
                     icon_url="https://i.imgur.com/96jPPXO.png")

    if status == 1:
        name = "Busted.."
        value = f"You lost **${bet}**."
        thumbnail_url = "https://i.imgur.com/rc68c43.png"
        color = discord.Color.red()
    
    elif status == 2:
        name = "You won with a score of 21!"
        value = f"You won **${payout}**."
        thumbnail_url = "https://i.imgur.com/dvIIr2G.png"
        color = discord.Color.green()

    elif status == 3:
        name = "The dealer busted. You won!"
        value = f"You won **${payout}**."
        thumbnail_url = "https://i.imgur.com/dvIIr2G.png"
        color = discord.Color.green()

    elif status == 4:
        name = "You lost.."
        value = f"You lost **${bet}**."
        thumbnail_url = "https://i.imgur.com/rc68c43.png"
        color = discord.Color.red()

    elif status == 5:
        name = "You won with a natural hand!"
        value = f"You won **${payout}**."
        thumbnail_url = "https://i.imgur.com/dvIIr2G.png"
        color = discord.Color.green()

    else:
        name = "I.. don't know if you won?"
        value = "This is an error, please report it."
        color = discord.Color.red()

    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)

    embed.add_field(name=name,
                    value=value,
                    inline=False)
    embed.colour = color

    return embed
