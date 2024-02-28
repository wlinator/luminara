import logging

from discord.ext import commands

from main import strings
from utils import checks

logs = logging.getLogger('Racu.Core')


class PingCog(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.slash_command(
        name="ping",
        description="Simple status check.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def ping(self, ctx):
        await ctx.respond(content=strings["ping"].format(ctx.author.name))


def setup(client):
    client.add_cog(PingCog(client))
