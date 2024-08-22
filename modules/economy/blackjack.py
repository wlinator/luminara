import random
from typing import List, Tuple

import discord
import pytz
from discord.ext import commands

from lib import interaction
from lib.constants import CONST
from lib.exceptions.LumiExceptions import LumiException
from services.currency_service import Currency
from services.stats_service import BlackJackStats
from lib.embed_builder import EmbedBuilder

EST = pytz.timezone("US/Eastern")
ACTIVE_BLACKJACK_GAMES: dict[int, bool] = {}

Card = str
Hand = List[Card]


async def cmd(ctx: commands.Context, bet: int) -> None:
    if ctx.author.id in ACTIVE_BLACKJACK_GAMES:
        raise LumiException(CONST.STRINGS["error_already_playing_blackjack"])

    currency = Currency(ctx.author.id)
    if bet > currency.balance:
        raise LumiException(CONST.STRINGS["error_not_enough_cash"])
    if bet <= 0:
        raise LumiException(CONST.STRINGS["error_invalid_bet"])

    ACTIVE_BLACKJACK_GAMES[ctx.author.id] = True

    try:
        await play_blackjack(ctx, currency, bet)
    except Exception as e:
        raise LumiException(CONST.STRINGS["error_blackjack_game_error"]) from e
    finally:
        del ACTIVE_BLACKJACK_GAMES[ctx.author.id]


async def play_blackjack(ctx: commands.Context, currency: Currency, bet: int) -> None:
    deck = get_new_deck()
    player_hand, dealer_hand = initial_deal(deck)
    multiplier = float(CONST.BLACKJACK["reward_multiplier"])

    player_value = calculate_hand_value(player_hand)
    status = 5 if player_value == 21 else 0
    view = interaction.BlackJackButtons(ctx)
    playing_embed = False

    while status == 0:
        dealer_value = calculate_hand_value(dealer_hand)

        embed = create_game_embed(
            ctx,
            bet,
            player_hand,
            dealer_hand,
            player_value,
            dealer_value,
        )
        if not playing_embed:
            await ctx.respond(embed=embed, view=view, content=ctx.author.mention)
            playing_embed = True
        else:
            await ctx.edit(embed=embed, view=view)

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
    return [deal_card(deck) for _ in range(2)], [deal_card(deck)]


def dealer_play(deck: List[Card], dealer_hand: Hand, player_value: int) -> int:
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
    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)
    payout = bet * (2 if status == 5 else multiplier)
    is_won = status not in [1, 4]

    embed = create_end_game_embed(ctx, bet, player_value, dealer_value, payout, status)

    if playing_embed:
        await ctx.edit(embed=embed, view=None)
    else:
        await ctx.respond(embed=embed, view=None, content=ctx.author.mention)

    currency.add_balance(payout) if is_won else currency.take_balance(bet)
    currency.push()

    BlackJackStats(
        user_id=ctx.author.id,
        is_won=is_won,
        bet=bet,
        payout=payout if is_won else 0,
        hand_player=player_hand,
        hand_dealer=dealer_hand,
    ).push()


def create_game_embed(
    ctx: commands.Context,
    bet: int,
    player_hand: Hand,
    dealer_hand: Hand,
    player_value: int,
    dealer_value: int,
) -> discord.Embed:
    player_hand_str = " + ".join(player_hand)
    dealer_hand_str = f"{dealer_hand[0]} + " + (
        CONST.STRINGS["blackjack_dealer_hidden"]
        if len(dealer_hand) < 2
        else " + ".join(dealer_hand[1:])
    )

    description = (
        f"{CONST.STRINGS['blackjack_player_hand'].format(player_value, player_hand_str)}\n\n"
        f"{CONST.STRINGS['blackjack_dealer_hand'].format(dealer_value, dealer_hand_str)}"
    )

    footer_text = (
        f"{CONST.STRINGS['blackjack_bet'].format(Currency.format_human(bet))} • "
        f"{CONST.STRINGS['blackjack_deck_shuffled']}"
    )

    return EmbedBuilder.create_embed(
        ctx,
        title=CONST.STRINGS["blackjack_title"],
        color=discord.Colour.embed_background(),
        description=description,
        footer_text=footer_text,
        footer_icon_url=CONST.MUFFIN_ART,
        show_name=False,
        hide_timestamp=True,
    )


def create_end_game_embed(
    ctx: commands.Context,
    bet: int,
    player_value: int,
    dealer_value: int,
    payout: int,
    status: int,
) -> discord.Embed:
    embed = EmbedBuilder.create_embed(
        ctx,
        title=CONST.STRINGS["blackjack_title"],
        color=discord.Colour.embed_background(),
        description=CONST.STRINGS["blackjack_description"].format(
            player_value,
            dealer_value,
        ),
        footer_text=CONST.STRINGS["blackjack_footer"],
        footer_icon_url=CONST.MUFFIN_ART,
        show_name=False,
    )

    result = {
        1: (
            CONST.STRINGS["blackjack_busted"],
            CONST.STRINGS["blackjack_lost"].format(Currency.format_human(bet)),
            discord.Color.red(),
            CONST.CLOUD_ART,
        ),
        2: (
            CONST.STRINGS["blackjack_won_21"],
            CONST.STRINGS["blackjack_won_payout"].format(Currency.format_human(payout)),
            discord.Color.green(),
            CONST.TROPHY_ART,
        ),
        3: (
            CONST.STRINGS["blackjack_dealer_busted"],
            CONST.STRINGS["blackjack_won_payout"].format(Currency.format_human(payout)),
            discord.Color.green(),
            CONST.TROPHY_ART,
        ),
        4: (
            CONST.STRINGS["blackjack_lost_generic"],
            CONST.STRINGS["blackjack_lost"].format(Currency.format_human(bet)),
            discord.Color.red(),
            CONST.CLOUD_ART,
        ),
        5: (
            CONST.STRINGS["blackjack_won_natural"],
            CONST.STRINGS["blackjack_won_payout"].format(Currency.format_human(payout)),
            discord.Color.green(),
            CONST.TROPHY_ART,
        ),
    }.get(
        status,
        (
            CONST.STRINGS["blackjack_error"],
            CONST.STRINGS["blackjack_error_description"],
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
    deck = [
        rank + suit
        for suit in CONST.BLACKJACK["deck_suits"]
        for rank in CONST.BLACKJACK["deck_ranks"]
    ]
    random.shuffle(deck)
    return deck


def deal_card(deck: List[Card]) -> Card:
    return deck.pop()


def calculate_hand_value(hand: Hand) -> int:
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
