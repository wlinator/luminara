import random
from datetime import datetime

import discord
import pytz
from discord.ext import commands
from loguru import logger

from lib import interaction
from lib.embeds.error import EconErrors
from services.currency_service import Currency
from services.stats_service import BlackJackStats
from lib.constants import CONST

est = pytz.timezone("US/Eastern")
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
        await ctx.respond(embed=EconErrors.already_playing(ctx))
        return

    # Currency handler
    ctx_currency = Currency(ctx.author.id)

    # check if the user has enough cash
    player_balance = ctx_currency.balance
    if bet > player_balance:
        raise commands.BadArgument("you don't have enough cash.")
    elif bet <= 0:
        raise commands.BadArgument("the bet you entered is invalid.")

    active_blackjack_games[ctx.author.id] = True

    try:
        deck = get_new_deck()
        multiplier = float(CONST.BLACKJACK["reward_multiplier"])

        player_hand = [deal_card(deck), deal_card(deck)]
        dealer_hand = [deal_card(deck)]
        # calculate initial hands
        player_hand_value = calculate_hand_value(player_hand)
        dealer_hand_value = calculate_hand_value(dealer_hand)

        status = 0 if player_hand_value != 21 else 5
        view = interaction.BlackJackButtons(ctx)
        playing_embed = False

        while status == 0:
            if not playing_embed:
                await ctx.respond(
                    embed=blackjack_show(
                        ctx,
                        Currency.format_human(bet),
                        player_hand,
                        dealer_hand,
                        player_hand_value,
                        dealer_hand_value,
                    ),
                    view=view,
                    content=ctx.author.mention,
                )

                playing_embed = True

            await view.wait()

            if view.clickedHit:
                # player draws a card & value is calculated
                player_hand.append(deal_card(deck))
                player_hand_value = calculate_hand_value(player_hand)

                if player_hand_value > 21:
                    status = 1
                    break
                elif player_hand_value == 21:
                    status = 2
                    break

            elif view.clickedStand:
                # player stands, dealer draws cards until he wins OR busts
                while dealer_hand_value <= player_hand_value:
                    dealer_hand.append(deal_card(deck))
                    dealer_hand_value = calculate_hand_value(dealer_hand)

                status = 3 if dealer_hand_value > 21 else 4
                break
            else:
                status = 6
                break

            # refresh
            view = interaction.BlackJackButtons(ctx)
            embed = blackjack_show(
                ctx,
                Currency.format_human(bet),
                player_hand,
                dealer_hand,
                player_hand_value,
                dealer_hand_value,
            )

            await ctx.edit(embed=embed, view=view, content=ctx.author.mention)

        """
        At this point the game has concluded, generate a final output & backend
        """
        payout = bet * 2 if status == 5 else bet * multiplier
        is_won = status not in [1, 4]

        embed = blackjack_finished(
            ctx,
            Currency.format_human(bet),
            player_hand_value,
            dealer_hand_value,
            Currency.format_human(payout),
            status,
        )

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
                hand_dealer=dealer_hand,
            )
            stats.push()

        elif status == 6:
            await ctx.send(
                embed=EconErrors.out_of_time(ctx),
                content=ctx.author.mention,
            )
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
                hand_dealer=dealer_hand,
            )
            stats.push()

    except Exception as e:
        # await ctx.respond(embed=GenericErrors.default_exception(ctx))
        logger.error("Something went wrong in the blackjack command: ", e)

    finally:
        # remove player from active games list
        del active_blackjack_games[ctx.author.id]


def blackjack_show(
    ctx,
    bet,
    player_hand,
    dealer_hand,
    player_hand_value,
    dealer_hand_value,
):
    current_time = datetime.now(est).strftime("%I:%M %p")
    embed = discord.Embed(
        title="BlackJack",
        color=discord.Color.dark_orange(),
    )

    embed.description = (
        f"**You**\n"
        f"Score: {player_hand_value}\n"
        f"*Hand: {' + '.join(player_hand)}*\n\n"
    )

    if len(dealer_hand) < 2:
        embed.description += (
            f"**Dealer**\n"
            f"Score: {dealer_hand_value}\n"
            f"*Hand: {dealer_hand[0]} + ??*"
        )
    else:
        embed.description += (
            f"**Dealer | Score: {dealer_hand_value}**\n"
            f"*Hand: {' + '.join(dealer_hand)}*"
        )

    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.set_footer(
        text=f"Bet ${bet} • deck shuffled • Today at {current_time}",
        icon_url="https://i.imgur.com/96jPPXO.png",
    )

    if thumbnail_url := None:
        embed.set_thumbnail(url=thumbnail_url)

    return embed


def blackjack_finished(ctx, bet, player_hand_value, dealer_hand_value, payout, status):
    current_time = datetime.now(est).strftime("%I:%M %p")
    thumbnail_url = None

    embed = discord.Embed(
        title="BlackJack",
    )
    embed.description = (
        f"You | Score: {player_hand_value}\n" f"Dealer | Score: {dealer_hand_value}"
    )
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.set_footer(
        text=f"Game finished • Today at {current_time}",
        icon_url="https://i.imgur.com/96jPPXO.png",
    )

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

    embed.add_field(
        name=name,
        value=value,
        inline=False,
    )
    embed.colour = color

    return embed


def get_new_deck():
    suits = CONST.BLACKJACK["deck_suits"]
    ranks = CONST.BLACKJACK["deck_ranks"]
    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append(rank + suit)
    random.shuffle(deck)
    return deck


def deal_card(deck):
    return deck.pop()


def calculate_hand_value(hand):
    value = 0
    has_ace = False
    aces_count = 0

    for card in hand:
        if card is None:
            continue

        rank = card[:-1]

        if rank.isdigit():
            value += int(rank)

        elif rank in ["J", "Q", "K"]:
            value += 10

        elif rank == "A":
            value += 11
            has_ace = True
            aces_count += 1

    """
    An Ace will have a value of 11 unless that would give a player 
    or the dealer a score in excess of 21; in which case, it has a value of 1
    """
    if value > 21 and has_ace:
        value -= 10 * aces_count

    return value
