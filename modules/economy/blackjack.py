import random
from datetime import datetime
from typing import List, Tuple

import discord
import pytz
from discord.ext import commands
from loguru import logger

from lib import interaction
from lib.constants import CONST
from lib.exceptions.LumiExceptions import LumiException
from services.currency_service import Currency
from services.stats_service import BlackJackStats

EST = pytz.timezone("US/Eastern")
ACTIVE_BLACKJACK_GAMES: dict[int, bool] = {}

Card = str
Hand = List[Card]


async def cmd(ctx: commands.Context, bet: int) -> None:
    """
    Handle the blackjack command.

    Args:
        ctx (commands.Context): The command context.
        bet (int): The amount of currency to bet.

    Raises:
        LumiException: If the player is already in a game.
        commands.BadArgument: If the bet is invalid or insufficient funds.
    """
    if ctx.author.id in ACTIVE_BLACKJACK_GAMES:
        raise LumiException(CONST.STRINGS["error_already_playing_blackjack"])

    currency = Currency(ctx.author.id)
    if bet > currency.balance:
        raise commands.BadArgument("You don't have enough cash.")
    if bet <= 0:
        raise commands.BadArgument("The bet you entered is invalid.")

    ACTIVE_BLACKJACK_GAMES[ctx.author.id] = True

    try:
        await play_blackjack(ctx, currency, bet)
    except Exception as e:
        logger.error(f"Error in blackjack command: {e}")
    finally:
        del ACTIVE_BLACKJACK_GAMES[ctx.author.id]


async def play_blackjack(ctx: commands.Context, currency: Currency, bet: int) -> None:
    """
    Play a game of blackjack.

    Args:
        ctx (commands.Context): The command context.
        currency (Currency): The player's currency service.
        bet (int): The amount bet.
    """
    deck = get_new_deck()
    player_hand, dealer_hand = initial_deal(deck)
    multiplier = float(CONST.BLACKJACK["reward_multiplier"])

    status = 0 if calculate_hand_value(player_hand) != 21 else 5
    view = interaction.BlackJackButtons(ctx)
    playing_embed = False

    while status == 0:
        player_value = calculate_hand_value(player_hand)
        dealer_value = calculate_hand_value(dealer_hand)

        if not playing_embed:
            await ctx.respond(
                embed=create_game_embed(
                    ctx,
                    bet,
                    player_hand,
                    dealer_hand,
                    player_value,
                    dealer_value,
                ),
                view=view,
                content=ctx.author.mention,
            )
            playing_embed = True
        else:
            await ctx.edit(
                embed=create_game_embed(
                    ctx,
                    bet,
                    player_hand,
                    dealer_hand,
                    player_value,
                    dealer_value,
                ),
                view=view,
            )

        await view.wait()

        if view.clickedHit:
            player_hand.append(deal_card(deck))
            player_value = calculate_hand_value(player_hand)
            if player_value > 21:
                status = 1
                break
            elif player_value == 21:
                status = 2
                break
        elif view.clickedStand:
            status = dealer_play(deck, dealer_hand, player_value)
            break
        else:
            currency.take_balance(bet)
            currency.push()
            raise LumiException(CONST.STRINGS["error_out_of_time_economy"])

        view = interaction.BlackJackButtons(ctx)

    await handle_game_end(
        ctx,
        currency,
        bet,
        player_hand,
        dealer_hand,
        status,
        multiplier,
        playing_embed,
    )


def initial_deal(deck: List[Card]) -> Tuple[Hand, Hand]:
    """
    Perform the initial deal for blackjack.

    Args:
        deck (List[Card]): The deck of cards.

    Returns:
        Tuple[Hand, Hand]: The player's hand and dealer's hand.
    """
    return [deal_card(deck), deal_card(deck)], [deal_card(deck)]


def dealer_play(deck: List[Card], dealer_hand: Hand, player_value: int) -> int:
    """
    Play the dealer's turn.

    Args:
        deck (List[Card]): The deck of cards.
        dealer_hand (Hand): The dealer's hand.
        player_value (int): The player's hand value.

    Returns:
        int: The game status after dealer's play.
    """
    while calculate_hand_value(dealer_hand) <= player_value:
        dealer_hand.append(deal_card(deck))
    return 3 if calculate_hand_value(dealer_hand) > 21 else 4


async def handle_game_end(
    ctx: commands.Context,
    currency: Currency,
    bet: int,
    player_hand: Hand,
    dealer_hand: Hand,
    status: int,
    multiplier: float,
    playing_embed: bool,
) -> None:
    """
    Handle the end of a blackjack game.

    Args:
        ctx (commands.Context): The command context.
        currency (Currency): The player's currency service.
        bet (int): The amount bet.
        player_hand (Hand): The player's final hand.
        dealer_hand (Hand): The dealer's final hand.
        status (int): The game status.
        multiplier (float): The payout multiplier.
        playing_embed (bool): Whether the game was played with embeds.
    """
    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)
    payout = bet * multiplier if status != 5 else bet * 2
    is_won = status not in [1, 4]

    embed = create_end_game_embed(ctx, bet, player_value, dealer_value, payout, status)

    if playing_embed:
        await ctx.edit(embed=embed, view=None)
    else:
        await ctx.respond(embed=embed, view=None, content=ctx.author.mention)

    if not is_won:
        currency.take_balance(bet)
    else:
        currency.add_balance(payout)
    currency.push()

    stats = BlackJackStats(
        user_id=ctx.author.id,
        is_won=is_won,
        bet=bet,
        payout=payout if is_won else 0,
        hand_player=player_hand,
        hand_dealer=dealer_hand,
    )
    stats.push()


def create_game_embed(
    ctx: commands.Context,
    bet: int,
    player_hand: Hand,
    dealer_hand: Hand,
    player_value: int,
    dealer_value: int,
) -> discord.Embed:
    """
    Create an embed for the current game state.

    Args:
        ctx (commands.Context): The command context.
        bet (int): The amount bet.
        player_hand (Hand): The player's hand.
        dealer_hand (Hand): The dealer's hand.
        player_value (int): The player's hand value.
        dealer_value (int): The dealer's hand value.

    Returns:
        discord.Embed: The game state embed.
    """
    current_time = datetime.now(EST).strftime("%I:%M %p")
    embed = discord.Embed(
        title="BlackJack",
        color=discord.Color.dark_orange(),
        description=(
            f"**You**\n"
            f"Score: {player_value}\n"
            f"*Hand: {' + '.join(player_hand)}*\n\n"
            f"**Dealer**\n"
            f"Score: {dealer_value}\n"
            f"*Hand: {dealer_hand[0]} + {'??' if len(dealer_hand) < 2 else ' + '.join(dealer_hand[1:])}*"
        ),
    )
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.set_footer(
        text=f"Bet ${Currency.format_human(bet)} • deck shuffled • Today at {current_time}",
        icon_url="https://i.imgur.com/96jPPXO.png",
    )
    return embed


def create_end_game_embed(
    ctx: commands.Context,
    bet: int,
    player_value: int,
    dealer_value: int,
    payout: int,
    status: int,
) -> discord.Embed:
    """
    Create an embed for the end of the game.

    Args:
        ctx (commands.Context): The command context.
        bet (int): The amount bet.
        player_value (int): The player's final hand value.
        dealer_value (int): The dealer's final hand value.
        payout (int): The payout amount.
        status (int): The game status.

    Returns:
        discord.Embed: The end game embed.
    """
    current_time = datetime.now(EST).strftime("%I:%M %p")
    embed = discord.Embed(
        title="BlackJack",
        description=f"You | Score: {player_value}\nDealer | Score: {dealer_value}",
    )
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.set_footer(
        text=f"Game finished • Today at {current_time}",
        icon_url="https://i.imgur.com/96jPPXO.png",
    )

    result = {
        1: (
            "Busted..",
            f"You lost **${Currency.format_human(bet)}**.",
            discord.Color.red(),
            "https://i.imgur.com/rc68c43.png",
        ),
        2: (
            "You won with a score of 21!",
            f"You won **${Currency.format_human(payout)}**.",
            discord.Color.green(),
            "https://i.imgur.com/dvIIr2G.png",
        ),
        3: (
            "The dealer busted. You won!",
            f"You won **${Currency.format_human(payout)}**.",
            discord.Color.green(),
            "https://i.imgur.com/dvIIr2G.png",
        ),
        4: (
            "You lost..",
            f"You lost **${Currency.format_human(bet)}**.",
            discord.Color.red(),
            "https://i.imgur.com/rc68c43.png",
        ),
        5: (
            "You won with a natural hand!",
            f"You won **${Currency.format_human(payout)}**.",
            discord.Color.green(),
            "https://i.imgur.com/dvIIr2G.png",
        ),
    }.get(
        status,
        (
            "I.. don't know if you won?",
            "This is an error, please report it.",
            discord.Color.red(),
            None,
        ),
    )

    name, value, color, thumbnail_url = result
    embed.add_field(name=name, value=value, inline=False)
    embed.colour = color
    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)

    return embed


def get_new_deck() -> List[Card]:
    """
    Create and shuffle a new deck of cards.

    Returns:
        List[Card]: A shuffled deck of cards.
    """
    deck = [
        rank + suit
        for suit in CONST.BLACKJACK["deck_suits"]
        for rank in CONST.BLACKJACK["deck_ranks"]
    ]
    random.shuffle(deck)
    return deck


def deal_card(deck: List[Card]) -> Card:
    """
    Deal a card from the deck.

    Args:
        deck (List[Card]): The deck of cards.

    Returns:
        Card: The dealt card.
    """
    return deck.pop()


def calculate_hand_value(hand: Hand) -> int:
    """
    Calculate the value of a hand in blackjack.

    Args:
        hand (Hand): The hand to calculate.

    Returns:
        int: The value of the hand.
    """
    value = sum(
        10 if rank in "JQK" else 11 if rank == "A" else int(rank)
        for card in hand
        for rank in card[:-1]
    )
    aces = sum(card[0] == "A" for card in hand)
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value
