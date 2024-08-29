import contextlib

import discord
from discord.ext import commands

from lib.const import CONST
from lib.exceptions import LumiException
from lib.format import format_duration_to_seconds
from ui.embeds import Builder


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
        arg1: str,
        arg2: str,
    ) -> None:
        # define actual channel & duration
        channel: discord.TextChannel | None = None
        duration: int | None = None

        for arg in (arg1, arg2):
            if not channel:
                try:
                    channel = await commands.TextChannelConverter().convert(ctx, arg)
                except commands.BadArgument:
                    with contextlib.suppress(LumiException):
                        duration = format_duration_to_seconds(arg)
            else:
                with contextlib.suppress(LumiException):
                    duration = format_duration_to_seconds(arg)

        if not channel:
            await ctx.send(CONST.STRINGS["slowmode_channel_not_found"])
            return

        if duration is None:
            await ctx.send(CONST.STRINGS["slowmode_duration_not_found"])
            return

        if duration < 0 or duration > 21600:  # 21600 seconds = 6 hours (Discord's max slowmode)
            await ctx.send("Slowmode duration must be between 0 and 21600 seconds.")
            return

        try:
            await channel.edit(slowmode_delay=duration)
            embed = Builder.create_embed(
                theme="success",
                user_name=ctx.author.name,
                author_text=CONST.STRINGS["slowmode_author"],
                description=CONST.STRINGS["slowmode_success"].format(duration, channel.mention),
                footer_text=CONST.STRINGS["slowmode_footer"],
            )
        except discord.Forbidden:
            embed = Builder.create_embed(
                theme="error",
                user_name=ctx.author.name,
                author_text=CONST.STRINGS["slowmode_author"],
                description=CONST.STRINGS["slowmode_forbidden"],
                footer_text=CONST.STRINGS["slowmode_footer"],
            )

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Slowmode(bot))
