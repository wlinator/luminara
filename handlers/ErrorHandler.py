import logging
import traceback
import sys

import discord
from discord.ext import commands
from lib.embeds.error import GenericErrors,BdayErrors
from lib.exceptions import RacuExceptions

logs = logging.getLogger('Racu.Core')


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
        if isinstance(error, RacuExceptions.NotAllowedInChannel):
            await ctx.respond(embed=GenericErrors.channel_not_allowed(ctx, error.command_channel),
                              delete_after=5, ephemeral=True)

        elif isinstance(error, RacuExceptions.BirthdaysDisabled):
            await ctx.respond(embed=BdayErrors.birthdays_disabled(ctx))

    else:
        await ctx.respond(embed=GenericErrors.default_exception(ctx))
        traceback.print_tb(error.__traceback__)

    logs.error(f"[CommandHandler] on_command_error: {error}")


async def on_error(event: str, *args, **kwargs) -> None:
    logs.error(f"[EventHandler] on_error INFO: errors.event.{event} | '*args': {args} | '**kwargs': {kwargs}")
    logs.error(f"[EventHandler] on_error EXCEPTION: {sys.exc_info()}")
    traceback.print_exc()