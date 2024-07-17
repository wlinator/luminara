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


def allowed_in_channel():
    async def predicate(ctx):
        if ctx.guild is None:
            return True

        guild_config = GuildConfig(ctx.guild.id)
        command_channel_id = guild_config.command_channel_id

        if command_channel_id:
            command_channel = await ctx.bot.get_or_fetch_channel(
                ctx.guild,
                command_channel_id,
            )

            if ctx.channel.id != command_channel_id and command_channel:
                raise LumiExceptions.NotAllowedInChannel(command_channel)

        return True

    return commands.check(predicate)
