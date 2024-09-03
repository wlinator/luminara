import random
from zoneinfo import ZoneInfo

import discord
from discord.ext import commands
from loguru import logger

import lib.format
from lib.client import Luminara
from lib.const import CONST
from lib.exceptions import LumiException
from services.currency_service import Currency
from services.stats_service import BlackJackStats
from ui.embeds import Builder
from ui.views.blackjack import BlackJackButtons

EST = ZoneInfo("US/Eastern")
ACTIVE_BLACKJACK_GAMES: dict[int, bool] = {}

Card = str
Hand = list[Card]


class Blackjack(commands.Cog):
    def __init__(self, bot: Luminara) -> None:
        self.bot: Luminara = bot
        self.blackjack.usage = lib.format.generate_usage(self.blackjack)

    @commands.hybrid_command(
        name="blackjack",
        aliases=["bj"],
    )
    @commands.guild_only()
    async def blackjack(
        self,
        ctx: commands.Context[Luminara],
        bet: int,
    ) -> None:
        """
        Play a game of blackjack.

        Parameters
        ----------
        ctx : commands.Context[Luminara]
            The context of the command.
        bet : int
            The amount to bet.
        """
        if ctx.author.id in ACTIVE_BLACKJACK_GAMES:
            raise LumiException(CONST.STRINGS["error_already_playing_blackjack"])

        currency = Currency(ctx.author.id)
        if bet > currency.balance:
            raise LumiException(CONST.STRINGS["error_not_enough_cash"])
        if bet <= 0:
            raise LumiException(CONST.STRINGS["error_invalid_bet"])

        ACTIVE_BLACKJACK_GAMES[ctx.author.id] = True

        try:
            await self.play_blackjack(ctx, currency, bet)
        except Exception as e:
            logger.exception(f"Error in blackjack game: {e}")
            raise LumiException(CONST.STRINGS["error_blackjack_game_error"]) from e
        finally:
            del ACTIVE_BLACKJACK_GAMES[ctx.author.id]

    async def play_blackjack(self, ctx: commands.Context[Luminara], currency: Currency, bet: int) -> None:
        deck = self.get_new_deck()
        player_hand, dealer_hand = self.initial_deal(deck)
        multiplier = CONST.BLACKJACK_MULTIPLIER

        player_value = self.calculate_hand_value(player_hand)
        status = 5 if player_value == 21 else 0
        view = BlackJackButtons(ctx)
        playing_embed = False
        response_message: discord.Message | None = None

        while status == 0:
            dealer_value = self.calculate_hand_value(dealer_hand)

            embed = self.create_game_embed(
                ctx,
                bet,
                player_hand,
                dealer_hand,
                player_value,
                dealer_value,
            )
            if not playing_embed:
                response_message = await ctx.reply(embed=embed, view=view)
                playing_embed = True
            else:
                assert response_message
                await response_message.edit(embed=embed, view=view)

            await view.wait()

            if view.clickedHit:
                player_hand.append(self.deal_card(deck))
                player_value = self.calculate_hand_value(player_hand)
                if player_value > 21:
                    status = 1
                    break
                if player_value == 21:
                    status = 2
                    break
            elif view.clickedStand:
                status = self.dealer_play(deck, dealer_hand, player_value)
                break
            else:
                currency.take_balance(bet)
                currency.push()
                raise LumiException(CONST.STRINGS["error_out_of_time_economy"])

            view = BlackJackButtons(ctx)

        await self.handle_game_end(
            ctx,
            response_message,
            currency,
            bet,
            player_hand,
            dealer_hand,
            status,
            multiplier,
            playing_embed,
        )

    def initial_deal(self, deck: list[Card]) -> tuple[Hand, Hand]:
        return [self.deal_card(deck) for _ in range(2)], [self.deal_card(deck)]

    def dealer_play(self, deck: list[Card], dealer_hand: Hand, player_value: int) -> int:
        while self.calculate_hand_value(dealer_hand) <= player_value:
            dealer_hand.append(self.deal_card(deck))
        return 3 if self.calculate_hand_value(dealer_hand) > 21 else 4

    async def handle_game_end(
        self,
        ctx: commands.Context[Luminara],
        response_message: discord.Message | None,
        currency: Currency,
        bet: int,
        player_hand: Hand,
        dealer_hand: Hand,
        status: int,
        multiplier: float,
        playing_embed: bool,
    ) -> None:
        player_value = self.calculate_hand_value(player_hand)
        dealer_value = self.calculate_hand_value(dealer_hand)
        payout = bet * (2 if status == 5 else multiplier)
        is_won = status not in [1, 4]

        embed = self.create_end_game_embed(ctx, bet, player_value, dealer_value, payout, status)
        if playing_embed:
            assert response_message
            await response_message.edit(embed=embed)
        else:
            await ctx.reply(embed=embed)

        if is_won:
            currency.add_balance(int(payout))
        else:
            currency.take_balance(bet)
        currency.push()

        BlackJackStats(
            user_id=ctx.author.id,
            is_won=is_won,
            bet=bet,
            payout=int(payout) if is_won else 0,
            hand_player=player_hand,
            hand_dealer=dealer_hand,
        ).push()

    def create_game_embed(
        self,
        ctx: commands.Context[Luminara],
        bet: int,
        player_hand: Hand,
        dealer_hand: Hand,
        player_value: int,
        dealer_value: int,
    ) -> discord.Embed:
        player_hand_str = " + ".join(player_hand)
        dealer_hand_str = f"{dealer_hand[0]} + " + (
            CONST.STRINGS["blackjack_dealer_hidden"] if len(dealer_hand) < 2 else " + ".join(dealer_hand[1:])
        )

        description = (
            f"{CONST.STRINGS['blackjack_player_hand'].format(player_value, player_hand_str)}\n\n"
            f"{CONST.STRINGS['blackjack_dealer_hand'].format(dealer_value, dealer_hand_str)}"
        )

        footer_text = (
            f"{CONST.STRINGS['blackjack_bet'].format(Currency.format_human(bet))} • "
            f"{CONST.STRINGS['blackjack_deck_shuffled']}"
        )

        return Builder.create_embed(
            theme="default",
            user_name=ctx.author.name,
            title=CONST.STRINGS["blackjack_title"],
            description=description,
            footer_text=footer_text,
            footer_icon_url=CONST.MUFFIN_ART,
            hide_name_in_description=True,
        )

    def create_end_game_embed(
        self,
        ctx: commands.Context[Luminara],
        bet: int,
        player_value: int,
        dealer_value: int,
        payout: int | float,
        status: int,
    ) -> discord.Embed:
        embed = Builder.create_embed(
            theme="default",
            user_name=ctx.author.name,
            title=CONST.STRINGS["blackjack_title"],
            description=CONST.STRINGS["blackjack_description"].format(
                player_value,
                dealer_value,
            ),
            footer_text=CONST.STRINGS["blackjack_footer"],
            footer_icon_url=CONST.MUFFIN_ART,
            hide_name_in_description=True,
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
                CONST.STRINGS["blackjack_won_payout"].format(Currency.format_human(int(payout))),
                discord.Color.green(),
                CONST.TROPHY_ART,
            ),
            3: (
                CONST.STRINGS["blackjack_dealer_busted"],
                CONST.STRINGS["blackjack_won_payout"].format(Currency.format_human(int(payout))),
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
                CONST.STRINGS["blackjack_won_payout"].format(Currency.format_human(int(payout))),
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

    def get_new_deck(self) -> list[Card]:
        deck = [
            rank + suit
            for suit in ["♠", "♡", "♢", "♣"]
            for rank in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        ]
        random.shuffle(deck)
        return deck

    def deal_card(self, deck: list[Card]) -> Card:
        return deck.pop()

    def calculate_hand_value(self, hand: Hand) -> int:
        value = sum(10 if rank in "JQK" else 11 if rank == "A" else int(rank) for card in hand for rank in card[:-1])
        aces = sum(card[0] == "A" for card in hand)
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value


async def setup(bot: Luminara) -> None:
    await bot.add_cog(Blackjack(bot))
