import datetime

import discord
from discord.ext import commands, bridge, tasks
from modules.moderation import ban
from lib import checks
from lib.embeds.info import MiscInfo
from modules.misc import introduction, invite, backup, info
from modules.config import prefix


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @bridge.bridge_command(
        name="ban",
        aliases=["b"]
    )
    @bridge.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban_command(self, ctx, target: discord.User, *, reason: str):
        await ban.user(self, ctx, target, reason)


def setup(client):
    client.add_cog(Moderation(client))
