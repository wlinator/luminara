import logging

import discord
from discord.ext import commands

from utils import checks

logs = logging.getLogger('Racu.Core')


class SayCog(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.slash_command(
        name="tess",
        description="Bot admin only",
        guild_only=True
    )
    @commands.check(checks.bot_owner)
    async def tess_command(self, ctx, *, txt: discord.Option(str)):
        await ctx.respond(content="✅", ephemeral=True)
        await ctx.send(content=txt)


def setup(client):
    client.add_cog(SayCog(client))
