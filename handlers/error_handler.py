import sys
import traceback
from loguru import logger
from discord.ext import commands

from lib.embeds.error import GenericErrors, BdayErrors
from lib.exceptions import LumiExceptions


# --- Error Handling Functions ---
async def handle_command_error(ctx, error):
    error_handlers = {
        commands.CommandNotFound: lambda: None,  # Ignore command not found
        commands.CommandOnCooldown: lambda: ctx.respond(
            embed=GenericErrors.command_on_cooldown(
                ctx, format_cooldown(error.retry_after)
            )
        ),
        commands.MissingPermissions: lambda: ctx.respond(
            embed=GenericErrors.missing_permissions(ctx)
        ),
        commands.BotMissingPermissions: lambda: ctx.respond(
            embed=GenericErrors.bot_missing_permissions(ctx)
        ),
        commands.PrivateMessageOnly: lambda: ctx.respond(
            embed=GenericErrors.private_message_only(ctx)
        ),
        commands.NoPrivateMessage: lambda: ctx.respond(
            embed=GenericErrors.guild_only(ctx)
        ),
        commands.NotOwner: lambda: ctx.respond(embed=GenericErrors.owner_only(ctx)),
        (commands.MissingRequiredArgument, commands.BadArgument): lambda: ctx.respond(
            embed=GenericErrors.bad_arg(ctx, error)
        ),
    }

    for error_type, handler in error_handlers.items():
        if isinstance(error, error_type):
            return await handler()

    # --- LumiExceptions ---
    if isinstance(error, LumiExceptions.NotAllowedInChannel):
        return await ctx.respond(
            content=f"You can only do that command in {error.command_channel.mention}.",
            ephemeral=True,
        )

    if isinstance(error, LumiExceptions.BirthdaysDisabled):
        return await ctx.respond(embed=BdayErrors.birthdays_disabled(ctx))

    # --- Default Exception Handling ---
    await ctx.respond(embed=GenericErrors.default_exception(ctx))
    log_error(
        f"on_command_error: errors.command.{ctx.command.qualified_name} | user: {ctx.author.name}"
    )


async def log_error(message):
    logger.error(message)
    logger.exception(f"EXCEPTION: {sys.exc_info()}")
    traceback.print_exc()


def format_cooldown(seconds):
    minutes = seconds // 60
    seconds %= 60
    return f"{int(minutes):02d}:{seconds:02d}"


# --- ErrorListener Cog ---
class ErrorListener(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if not isinstance(error, LumiExceptions.NotAllowedInChannel):
            await handle_command_error(ctx, error)

        log_message = f"{ctx.author.name} executed .{ctx.command.qualified_name} "
        log_message += f" | guild: {ctx.guild.name} " if ctx.guild else "in DMs "
        log_message += (
            f"| FAILED: {f'{str(error)[:80]}...' if len(str(error)) > 80 else error}"
        )
        logger.warning(log_message)

    @commands.Cog.listener()  # Listen for slash command errors
    async def on_application_command_error(self, ctx, error):
        await self.on_command_error(ctx, error)  # Reuse the same handler

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        log_error(
            f"on_error INFO: errors.event.{event} | '*args': {args} | '**kwargs': {kwargs}"
        )


# --- Cog Setup ---
def setup(client):
    client.add_cog(ErrorListener(client))
