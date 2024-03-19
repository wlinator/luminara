import logging

import discord
from discord.ext import commands

from lib import checks

logs = logging.getLogger('Racu.Core')


class SayCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        name="say",
        description="Bot admin only.",
        guild_only=True
    )
    @commands.is_owner()
    @commands.guild_only()
    async def say(self, ctx, *, txt: discord.Option(str)):
        await ctx.respond(content="✅", ephemeral=True)
        await ctx.send(content=txt)


def setup(client):
    client.add_cog(SayCog(client))
