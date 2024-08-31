import contextlib

import discord
from discord import app_commands
from discord.ext import commands

from lib.const import CONST
from lib.exceptions import LumiException
from lib.format import format_duration_to_seconds


class Slowmode(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _set_slowmode(
        self,
        ctx: commands.Context[commands.Bot] | discord.Interaction,
        channel: discord.TextChannel,
        duration: str | None,
    ) -> None:
        if duration is None:
            await self._send_response(
                ctx,
                CONST.STRINGS["slowmode_current_value"].format(channel.mention, channel.slowmode_delay),
            )
            return

        try:
            seconds = format_duration_to_seconds(duration)
        except LumiException:
            await self._send_response(ctx, CONST.STRINGS["slowmode_invalid_duration"], ephemeral=True)
            return

        if not 0 <= seconds <= 21600:  # 21600 seconds = 6 hours (Discord's max slowmode)
            await self._send_response(ctx, CONST.STRINGS["slowmode_invalid_duration"], ephemeral=True)
            return

        try:
            await channel.edit(slowmode_delay=seconds)
            await self._send_response(ctx, CONST.STRINGS["slowmode_success"].format(seconds, channel.mention))
        except discord.Forbidden:
            await self._send_response(ctx, CONST.STRINGS["slowmode_forbidden"], ephemeral=True)

    async def _send_response(
        self,
        ctx: commands.Context[commands.Bot] | discord.Interaction,
        content: str,
        ephemeral: bool = False,
    ) -> None:
        if isinstance(ctx, commands.Context):
            await ctx.send(content)
        else:
            await ctx.response.send_message(content, ephemeral=ephemeral)

    @commands.command(
        name="slowmode",
        aliases=["sm"],
    )
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.guild_only()
    async def slowmode(
        self,
        ctx: commands.Context[commands.Bot],
        arg1: str | None = None,
        arg2: str | None = None,
    ) -> None:
        """
        Set or view the slowmode for a channel.

        Parameters
        ----------
        arg1: str | None
            The first argument. Defaults to None.
        arg2: str | None
            The second argument. Defaults to None.
        """
        channel, duration = None, None

        for arg in (arg1, arg2):
            if not channel and arg:
                with contextlib.suppress(commands.BadArgument):
                    channel = await commands.TextChannelConverter().convert(ctx, arg)
                    continue
            if arg:
                duration = arg

        if not channel:
            await ctx.send(CONST.STRINGS["slowmode_channel_not_found"])
            return

        await self._set_slowmode(ctx, channel, duration)

    @app_commands.command(
        name="slowmode",
    )
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.checks.bot_has_permissions(manage_channels=True)
    @app_commands.guild_only()
    async def slowmode_slash(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        duration: str | None = None,
    ) -> None:
        """
        Set or view the slowmode for a channel.

        Parameters
        ----------
        channel: discord.TextChannel
            The channel to set the slowmode for.
        duration: str | None
            The duration of the slowmode. Defaults to None.
        """
        await self._set_slowmode(interaction, channel, duration)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Slowmode(bot))
