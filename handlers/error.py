import sys
import traceback

from discord.ext import commands
from discord.ext.commands import Cog
from loguru import logger

from lib.const import CONST
from ui.embeds import builder
from lib import exceptions as LumiExceptions


async def handle_error(
    ctx: commands.Context[commands.Bot],
    error: commands.CommandError | commands.CheckFailure,
) -> None:
    if isinstance(error, (commands.CommandNotFound, LumiExceptions.Blacklisted)):
        return

    author_text = None
    description = None
    footer_text = None
    ephemeral = False

    if isinstance(error, commands.MissingRequiredArgument):
        author_text = CONST.STRINGS["error_bad_argument_author"]
        description = CONST.STRINGS["error_bad_argument_description"].format(str(error))

    elif isinstance(error, commands.BadArgument):
        author_text = CONST.STRINGS["error_bad_argument_author"]
        description = CONST.STRINGS["error_bad_argument_description"].format(str(error))

    elif isinstance(error, commands.BotMissingPermissions):
        author_text = CONST.STRINGS["error_bot_missing_permissions_author"]
        description = CONST.STRINGS["error_bot_missing_permissions_description"]

    elif isinstance(error, commands.CommandOnCooldown):
        author_text = CONST.STRINGS["error_command_cooldown_author"]
        description = CONST.STRINGS["error_command_cooldown_description"].format(
            int(error.retry_after // 60),
            int(error.retry_after % 60),
        )
        ephemeral = True

    elif isinstance(error, commands.MissingPermissions):
        author_text = CONST.STRINGS["error_missing_permissions_author"]
        description = CONST.STRINGS["error_missing_permissions_description"]

    elif isinstance(error, commands.NoPrivateMessage):
        author_text = CONST.STRINGS["error_no_private_message_author"]
        description = CONST.STRINGS["error_no_private_message_description"]

    elif isinstance(error, commands.NotOwner):
        author_text = CONST.STRINGS["error_not_owner_author"]
        description = CONST.STRINGS["error_not_owner_description"]

    elif isinstance(error, commands.PrivateMessageOnly):
        author_text = CONST.STRINGS["error_private_message_only_author"]
        description = CONST.STRINGS["error_private_message_only_description"]

    elif isinstance(error, LumiExceptions.BirthdaysDisabled):
        author_text = CONST.STRINGS["error_birthdays_disabled_author"]
        description = CONST.STRINGS["error_birthdays_disabled_description"]
        footer_text = CONST.STRINGS["error_birthdays_disabled_footer"]

    elif isinstance(error, LumiExceptions.LumiException):
        author_text = CONST.STRINGS["error_lumi_exception_author"]
        description = CONST.STRINGS["error_lumi_exception_description"].format(
            str(error),
        )

    else:
        author_text = CONST.STRINGS["error_unknown_error_author"]
        description = CONST.STRINGS["error_unknown_error_description"]

    await ctx.send(
        embed=builder.create_embed(
            theme="error",
            user_name=ctx.author.name,
            author_text=author_text,
            description=description,
            footer_text=footer_text,
        ),
        ephemeral=ephemeral,
    )


async def on_error(event: str, *args, **kwargs) -> None:
    logger.exception(
        f"on_error INFO: errors.event.{event} | '*args': {args} | '**kwargs': {kwargs}",
    )
    logger.exception(f"on_error EXCEPTION: {sys.exc_info()}")
    traceback.print_exc()


class ErrorHandler(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @staticmethod
    async def log_command_error(ctx, error, command_type):
        log_msg = (
            f"{ctx.author.name} executed {command_type}{ctx.command.qualified_name}"
        )

        log_msg += " in DMs" if ctx.guild is None else f" | guild: {ctx.guild.name} "
        logger.exception(f"{log_msg} | FAILED: {error}")

    @Cog.listener()
    async def on_command_error(
        self,
        ctx: commands.Context[commands.Bot],
        error: commands.CommandError | commands.CheckFailure,
    ) -> None:
        try:
            await handle_error(ctx, error)
            await self.log_command_error(ctx, error, ".")
        except Exception as e:
            logger.exception(f"Error in on_command_error: {e}")
            traceback.print_exc()

    @Cog.listener()
    async def on_app_command_error(
        self,
        ctx: commands.Context[commands.Bot],
        error: commands.CommandError | commands.CheckFailure,
    ) -> None:
        try:
            await handle_error(ctx, error)
            await self.log_command_error(ctx, error, "/")
        except Exception as e:
            logger.exception(f"Error in on_app_command_error: {e}")
            traceback.print_exc()

    @Cog.listener()
    async def on_error(self, event: str, *args, **kwargs) -> None:
        await on_error(event, *args, **kwargs)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ErrorHandler(bot))