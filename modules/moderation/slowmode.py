import contextlib

import discord
from discord.ext import commands

from lib.const import CONST
from lib.exceptions import LumiException
from lib.format import format_duration_to_seconds


class Slowmode(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        name="slowmode",
        aliases=["sm"],
        usage="slowmode <duration> <channel>",
    )
    @commands.has_permissions(manage_channels=True)
    async def slowmode(
        self,
        ctx: commands.Context[commands.Bot],
        arg1: str | None = None,
        arg2: str | None = None,
    ) -> None:
        channel, duration = None, None

        for arg in (arg1, arg2):
            if not channel and arg:
                with contextlib.suppress(commands.BadArgument):
                    channel = await commands.TextChannelConverter().convert(ctx, arg)
                    continue
            if arg:
                with contextlib.suppress(LumiException):
                    duration = format_duration_to_seconds(arg)
        if not channel:
            await ctx.send(CONST.STRINGS["slowmode_channel_not_found"])
            return

        if duration is None:
            current_slowmode = channel.slowmode_delay
            await ctx.send(CONST.STRINGS["slowmode_current_value"].format(channel.mention, current_slowmode))
            return

        if duration < 0 or duration > 21600:  # 21600 seconds = 6 hours (Discord's max slowmode)
            await ctx.send(CONST.STRINGS["slowmode_duration_error"])
            return

        try:
            await channel.edit(slowmode_delay=duration)
            await ctx.send(CONST.STRINGS["slowmode_success"].format(duration, channel.mention))
        except discord.Forbidden as error:
            raise LumiException(CONST.STRINGS["slowmode_forbidden"]) from error


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Slowmode(bot))
