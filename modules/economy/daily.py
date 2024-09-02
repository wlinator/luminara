from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from discord import Embed
from discord.ext import commands

import lib.format
from lib.const import CONST
from services.currency_service import Currency
from services.daily_service import Dailies
from ui.embeds import Builder

tz = ZoneInfo("US/Eastern")


def seconds_until(hours: int, minutes: int) -> int:
    now = datetime.now(tz)
    given_time = now.replace(hour=hours, minute=minutes, second=0, microsecond=0)

    if given_time < now:
        given_time += timedelta(days=1)

    return int((given_time - now).total_seconds())


class Daily(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.daily.usage = lib.format.generate_usage(self.daily)

    @commands.hybrid_command(
        name="daily",
        aliases=["timely"],
    )
    @commands.guild_only()
    async def daily(
        self,
        ctx: commands.Context[commands.Bot],
    ) -> None:
        """
        Claim your daily reward.

        Parameters
        ----------
        ctx : commands.Context[commands.Bot]
            The context of the command.
        """
        ctx_daily: Dailies = Dailies(ctx.author.id)

        if not ctx_daily.can_be_claimed():
            wait_time: datetime = datetime.now(tz) + timedelta(seconds=seconds_until(7, 0))
            unix_time: int = int(round(wait_time.timestamp()))
            error_embed: Embed = Builder.create_embed(
                theme="error",
                user_name=ctx.author.name,
                author_text=CONST.STRINGS["daily_already_claimed_author"],
                description=CONST.STRINGS["daily_already_claimed_description"].format(
                    unix_time,
                ),
                footer_text=CONST.STRINGS["daily_already_claimed_footer"],
            )
            await ctx.send(embed=error_embed)
            return

        ctx_daily.streak = ctx_daily.streak + 1 if ctx_daily.streak_check() else 1
        ctx_daily.claimed_at = datetime.now(tz=ctx_daily.tz)
        ctx_daily.amount = 100 * 12 * (ctx_daily.streak - 1)

        ctx_daily.refresh()

        embed: Embed = Builder.create_embed(
            theme="success",
            user_name=ctx.author.name,
            author_text=CONST.STRINGS["daily_success_claim_author"],
            description=CONST.STRINGS["daily_success_claim_description"].format(
                Currency.format(ctx_daily.amount),
            ),
            footer_text=CONST.STRINGS["daily_streak_footer"].format(ctx_daily.streak) if ctx_daily.streak > 1 else None,
        )

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Daily(bot))
