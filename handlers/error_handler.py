import sys
import traceback
from loguru import logger

import discord
from discord.ext import commands
from discord.ext.commands import Cog

from lib.embeds.error import GenericErrors, BdayErrors
from lib.exceptions import LumiExceptions


async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass

    elif isinstance(error, commands.CommandOnCooldown):
        seconds = error.retry_after
        minutes = seconds // 60
        seconds %= 60
        cooldown = "{:02d}:{:02d}".format(int(minutes), int(seconds))

        await ctx.respond(embed=GenericErrors.command_on_cooldown(ctx, cooldown))

    elif isinstance(error, commands.MissingPermissions):
        await ctx.respond(embed=GenericErrors.missing_permissions(ctx))

    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.respond(embed=GenericErrors.bot_missing_permissions(ctx))

    elif isinstance(error, commands.PrivateMessageOnly):
        await ctx.respond(embed=GenericErrors.private_message_only(ctx))

    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.respond(embed=GenericErrors.guild_only(ctx))

    elif isinstance(error, commands.NotOwner):
        await ctx.respond(embed=GenericErrors.owner_only(ctx))

    elif isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument)):
        return await ctx.respond(embed=GenericErrors.bad_arg(ctx, error))

    elif isinstance(error, (discord.CheckFailure, commands.CheckFailure)):
        """subclasses of this exception"""
        if isinstance(error, LumiExceptions.NotAllowedInChannel):
            await ctx.respond(
                content=f"You can only do that command in {error.command_channel.mention}.",
                ephemeral=True,
            )

        elif isinstance(error, LumiExceptions.BirthdaysDisabled):
            await ctx.respond(embed=BdayErrors.birthdays_disabled(ctx))

    else:
        await ctx.respond(embed=GenericErrors.default_exception(ctx))
        logger.error(
            f"on_command_error: errors.command.{ctx.command.qualified_name} | user: {ctx.author.name}"
        )


async def on_error(event: str, *args, **kwargs) -> None:
    logger.exception(
        f"on_error INFO: errors.event.{event} | '*args': {args} | '**kwargs': {kwargs}"
    )
    logger.exception(f"on_error EXCEPTION: {sys.exc_info()}")
    traceback.print_exc()


class ErrorListener(Cog):
    def __init__(self, client):
        self.client = client

    # @Cog.listener()
    # async def on_command_error(self, ctx, error) -> None:

    #     # on a prefix command, don't send anything if channel check fails. (to prevent spam in non-bot channels)
    #     # current issues with this: await ctx.trigger_typing() is still invoked for 10 seconds.
    #     if not isinstance(error, LumiExceptions.NotAllowedInChannel):
    #         await on_command_error(ctx, error)

    #     log_msg = '%s executed .%s' % (ctx.author.name, ctx.command.qualified_name)

    #     if ctx.guild is not None:
    #         log_msg += f" | guild: {ctx.guild.name} "
    #     else:
    #         log_msg += " in DMs"

    #     # make error shorter than full screen width
    #     if len(str(error)) > 80:
    #         error = str(error)[:80] + "..."
    #     logger.warning(f"{log_msg} | FAILED: {error}")

    # @Cog.listener()
    # async def on_application_command_error(self, ctx, error) -> None:
    #     await on_command_error(ctx, error)
    #     log_msg = '%s executed /%s' % (ctx.author.name, ctx.command.qualified_name)

    #     if ctx.guild is not None:
    #         log_msg += f" | guild: {ctx.guild.name} "
    #     else:
    #         log_msg += " in DMs"

    #     # make error shorter than full screen width
    #     if len(str(error)) > 80:
    #         error = str(error)[:80] + "..."
    #     logger.warning(f"{log_msg} | FAILED: {error}")

    # @Cog.listener()
    # async def on_error(self, event: str, *args, **kwargs) -> None:
    #     await on_error(event, *args, **kwargs)


def setup(client):
    client.add_cog(ErrorListener(client))
