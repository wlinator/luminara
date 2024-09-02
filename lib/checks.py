import discord
from discord import app_commands

from lib.exceptions import BirthdaysDisabled
from services.config_service import GuildConfig


def birthdays_enabled():
    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.guild is None:
            return True

        guild_config = GuildConfig(interaction.guild.id)
        if guild_config.birthday_channel_id is None:
            raise BirthdaysDisabled

        return True

    return app_commands.check(predicate)
