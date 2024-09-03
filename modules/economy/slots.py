import asyncio
import datetime
import random
from collections import Counter
from zoneinfo import ZoneInfo

import discord
from discord.ext import commands

import lib.format
from lib.client import Luminara
from lib.const import CONST
from lib.exceptions import LumiException
from services.currency_service import Currency
from services.stats_service import SlotsStats

est = ZoneInfo("US/Eastern")


class Slots(commands.Cog):
    def __init__(self, bot: Luminara) -> None:
        self.bot: Luminara = bot
        self.slots.usage = lib.format.generate_usage(self.slots)

    @commands.hybrid_command(
        name="slots",
        aliases=["slot"],
    )
    @commands.guild_only()
    async def slots(
        self,
        ctx: commands.Context[Luminara],
        bet: int,
    ) -> None:
        """
        Play the slots machine.

        Parameters
        ----------
        ctx : commands.Context[Luminara]
            The context of the command.
        bet : int
            The amount to bet.
        """
        ctx_currency: Currency = Currency(ctx.author.id)

        player_balance: int = ctx_currency.balance
        if bet > player_balance:
            raise LumiException(CONST.STRINGS["error_not_enough_cash"])
        if bet <= 0:
            raise LumiException(CONST.STRINGS["error_invalid_bet"])

        results: list[int] = [random.randint(0, 6) for _ in range(3)]
        calculated_results: tuple[str, int, float] = self.calculate_slots_results(bet, results)

        result_type, payout, _ = calculated_results
        is_won: bool = result_type != "lost"
        emojis: dict[str, discord.Emoji | None] = self.get_emotes()

        await ctx.defer()

        message: discord.Message = await ctx.reply(
            embed=self.slots_spinning(ctx, 3, Currency.format_human(bet), results, emojis),
        )

        for i in range(2, 0, -1):
            await asyncio.sleep(1)
            await message.edit(
                embed=self.slots_spinning(ctx, i, Currency.format_human(bet), results, emojis),
            )

        # output final result
        finished_output: discord.Embed = self.slots_finished(
            ctx,
            result_type,
            Currency.format_human(bet),
            Currency.format_human(payout),
            results,
            emojis,
        )

        await asyncio.sleep(1)
        await message.edit(embed=finished_output)

        # user payout
        if payout > 0:
            ctx_currency.add_balance(payout)
        else:
            ctx_currency.take_balance(bet)

        stats: SlotsStats = SlotsStats(
            user_id=ctx.author.id,
            is_won=is_won,
            bet=bet,
            payout=payout,
            spin_type=result_type,
            icons=[str(icon) for icon in results],
        )

        ctx_currency.push()
        stats.push()

    def get_emotes(self) -> dict[str, discord.Emoji | None]:
        emotes: dict[str, int] = CONST.EMOTE_IDS
        return {name: self.bot.get_emoji(emoji_id) for name, emoji_id in emotes.items()}

    def calculate_slots_results(self, bet: int, results: list[int]) -> tuple[str, int, float]:
        result_type: str = "lost"
        multiplier: float = 0.0
        rewards: dict[str, float] = CONST.SLOTS_MULTIPLIERS

        # count occurrences of each item in the list
        counts: Counter[int] = Counter(results)

        # no icons match
        if len(counts) == 3:
            result_type = "lost"
            multiplier = 0.0

        elif len(counts) == 2:
            result_type = "pair"
            multiplier = rewards[result_type]

        elif len(counts) == 1:
            if results[0] == 5:
                result_type = "three_diamonds"
            elif results[0] == 6:
                result_type = "jackpot"
            else:
                result_type = "three_of_a_kind"
            multiplier = rewards[result_type]

        payout: int = int(bet * multiplier)
        return result_type, payout, multiplier

    def slots_spinning(
        self,
        ctx: commands.Context[Luminara],
        spinning_icons_amount: int,
        bet: str,
        results: list[int],
        emojis: dict[str, discord.Emoji | None],
    ) -> discord.Embed:
        first_slots_emote: discord.Emoji | None = emojis.get(f"slots_{results[0]}_id")
        second_slots_emote: discord.Emoji | None = emojis.get(f"slots_{results[1]}_id")
        slots_animated_emote: discord.Emoji | None = emojis.get("slots_animated_id")

        current_time: str = datetime.datetime.now(est).strftime("%I:%M %p")
        one: discord.Emoji | None = slots_animated_emote
        two: discord.Emoji | None = slots_animated_emote
        three: discord.Emoji | None = slots_animated_emote

        if spinning_icons_amount == 1:
            one = first_slots_emote
            two = second_slots_emote

        elif spinning_icons_amount == 2:
            one = first_slots_emote
        description: str = (
            f"🎰{emojis['S_Wide']}{emojis['L_Wide']}{emojis['O_Wide']}{emojis['T_Wide']}{emojis['S_Wide']}🎰\n"
            f"{emojis['CBorderTLeft']}{emojis['HBorderT']}{emojis['HBorderT']}{emojis['HBorderT']}"
            f"{emojis['HBorderT']}{emojis['HBorderT']}{emojis['CBorderTRight']}\n"
            f"{emojis['VBorder']}{one}{emojis['VBorder']}{two}{emojis['VBorder']}"
            f"{three}{emojis['VBorder']}\n"
            f"{emojis['CBorderBLeft']}{emojis['HBorderB']}{emojis['HBorderB']}{emojis['HBorderB']}"
            f"{emojis['HBorderB']}{emojis['HBorderB']}{emojis['CBorderBRight']}\n"
            f"{emojis['Blank']}{emojis['Blank']}❓❓❓{emojis['Blank']}{emojis['Blank']}{emojis['Blank']}"
        )

        embed: discord.Embed = discord.Embed(
            description=description,
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.set_footer(
            text=f"Bet ${bet} • jackpot = x15 • {current_time}",
            icon_url="https://i.imgur.com/wFsgSnr.png",
        )

        return embed

    def slots_finished(
        self,
        ctx: commands.Context[Luminara],
        payout_type: str,
        bet: str,
        payout: str,
        results: list[int],
        emojis: dict[str, discord.Emoji | None],
    ) -> discord.Embed:
        first_slots_emote: discord.Emoji | None = emojis.get(f"slots_{results[0]}_id")
        second_slots_emote: discord.Emoji | None = emojis.get(f"slots_{results[1]}_id")
        third_slots_emote: discord.Emoji | None = emojis.get(f"slots_{results[2]}_id")
        current_time: str = datetime.datetime.now(est).strftime("%I:%M %p")

        field_name: str = "You lost."
        field_value: str = f"You lost **${bet}**."
        color: discord.Color = discord.Color.red()
        is_lost: bool = True

        if payout_type == "pair":
            field_name = "Pair"
            field_value = f"You won **${payout}**."
            is_lost = False
            color = discord.Color.dark_green()
        elif payout_type == "three_of_a_kind":
            field_name = "3 of a kind"
            field_value = f"You won **${payout}**."
            is_lost = False
            color = discord.Color.dark_green()
        elif payout_type == "three_diamonds":
            field_name = "Triple Diamonds!"
            field_value = f"You won **${payout}**."
            is_lost = False
            color = discord.Color.green()
        elif payout_type == "jackpot":
            field_name = "JACKPOT!!"
            field_value = f"You won **${payout}**."
            is_lost = False
            color = discord.Color.green()

        description: str = (
            f"🎰{emojis['S_Wide']}{emojis['L_Wide']}{emojis['O_Wide']}{emojis['T_Wide']}{emojis['S_Wide']}🎰\n"
            f"{emojis['CBorderTLeft']}{emojis['HBorderT']}{emojis['HBorderT']}{emojis['HBorderT']}"
            f"{emojis['HBorderT']}{emojis['HBorderT']}{emojis['CBorderTRight']}\n"
            f"{emojis['VBorder']}{first_slots_emote}{emojis['VBorder']}{second_slots_emote}"
            f"{emojis['VBorder']}{third_slots_emote}{emojis['VBorder']}\n"
            f"{emojis['CBorderBLeft']}{emojis['HBorderB']}{emojis['HBorderB']}{emojis['HBorderB']}"
            f"{emojis['HBorderB']}{emojis['HBorderB']}{emojis['CBorderBRight']}"
        )

        if is_lost:
            description += (
                f"\n{emojis['Blank']}{emojis['LCentered']}{emojis['OCentered']}{emojis['SCentered']}"
                f"{emojis['ECentered']}{emojis['lost']}{emojis['Blank']}"
            )
        else:
            description += (
                f"\n{emojis['Blank']}🎉{emojis['WSmall']}{emojis['ISmall']}{emojis['NSmall']}🎉{emojis['Blank']}"
            )

        embed: discord.Embed = discord.Embed(
            color=color,
            description=description,
        )
        embed.add_field(name=field_name, value=field_value, inline=False)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.set_footer(
            text=f"Game finished • {current_time}",
            icon_url="https://i.imgur.com/wFsgSnr.png",
        )

        return embed


async def setup(bot: Luminara) -> None:
    await bot.add_cog(Slots(bot))
