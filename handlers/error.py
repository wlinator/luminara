import sys
import traceback
from typing import Any

import discord
from discord import app_commands
from discord.ext import commands
from loguru import logger

from lib import exceptions
from lib.const import CONST

error_map: dict[type[Exception], str] = {
    commands.BotMissingPermissions: CONST.STRINGS["error_bot_missing_permissions_description"],
    commands.MissingPermissions: CONST.STRINGS["error_missing_permissions_description"],
    commands.NoPrivateMessage: CONST.STRINGS["error_no_private_message_description"],
    commands.NotOwner: CONST.STRINGS["error_not_owner_unknown"],
    commands.PrivateMessageOnly: CONST.STRINGS["error_private_message_only_description"],
    exceptions.BirthdaysDisabled: CONST.STRINGS["error_birthdays_disabled_description"],
}


async def on_error(event: str, *args: Any, **kwargs: Any) -> None:
    logger.exception(
        f"on_error INFO: errors.event.{event} | '*args': {args} | '**kwargs': {kwargs}",
    )
    logger.exception(f"on_error EXCEPTION: {sys.exc_info()}")
    traceback.print_exc()


async def log_command_error(
    user_name: str,
    command_name: str | None,
    guild_name: str | None,
    error: commands.CommandError | commands.CheckFailure | app_commands.AppCommandError,
    command_type: str,
) -> None:
    if isinstance(error, commands.NotOwner | exceptions.Blacklisted):
        return

    log_msg = f"{user_name} executed {command_type}{command_name or 'Unknown'}"

    log_msg += " in DMs" if guild_name is None else f" | guild: {guild_name} "
    logger.error(f"{log_msg} | FAILED: {error}")


class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def cog_load(self):
        tree = self.bot.tree
        self._old_tree_error = tree.on_error
        tree.on_error = self.on_app_command_error

    async def on_app_command_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ) -> None:
        if isinstance(error, commands.CommandNotFound | exceptions.Blacklisted):
            return

        await log_command_error(
            user_name=interaction.user.name,
            command_name=interaction.command.qualified_name if interaction.command else None,
            guild_name=interaction.guild.name if interaction.guild else None,
            error=error,
            command_type="/",
        )

        error_msg = error_map.get(type(error), str(error))
        await interaction.response.send_message(content=f"❌ **{interaction.user.name}** {error_msg}", ephemeral=True)

    @commands.Cog.listener()
    async def on_command_error(
        self,
        ctx: commands.Context[commands.Bot],
        error: commands.CommandError | commands.CheckFailure,
    ) -> None:
        if isinstance(error, commands.CommandNotFound | exceptions.Blacklisted):
            return

        await log_command_error(
            user_name=ctx.author.name,
            command_name=ctx.command.qualified_name if ctx.command else None,
            guild_name=ctx.guild.name if ctx.guild else None,
            error=error,
            command_type=".",
        )

        error_msg = error_map.get(type(error), str(error))
        await ctx.send(content=f"❌ **{ctx.author.name}** {error_msg}")

    @commands.Cog.listener()
    async def on_error(self, event: str, *args: Any, **kwargs: Any) -> None:
        await on_error(event, *args, **kwargs)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ErrorHandler(bot))
