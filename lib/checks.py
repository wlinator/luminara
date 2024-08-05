from discord.ext import commands

from lib.exceptions import LumiExceptions
from services.config_service import GuildConfig


def birthdays_enabled():
    async def predicate(ctx):
        if ctx.guild is None:
            return True

        guild_config = GuildConfig(ctx.guild.id)

        if not guild_config.birthday_channel_id:
            raise LumiExceptions.BirthdaysDisabled

        return True

    return commands.check(predicate)
