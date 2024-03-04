import logging

import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from services.GuildConfig import GuildConfig

from main import strings

logs = logging.getLogger('Racu.Core')

class ConfigCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    config = SlashCommandGroup("config", "server config commands.", guild_only=True, default_member_permissions=discord.Permissions(manage_guild=True))
    birthday_config = config.create_subgroup(name="birthdays")

    @birthday_config.command(
        name="disable",
        description="Disables birthday commands and announcements.",
        guild_only=True
    )
    async def config_birthdays_disable(self, ctx):
        


def setup(client):
    client.add_cog(ConfigCog(client))
