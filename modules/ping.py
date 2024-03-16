import logging

from discord.ext import commands, bridge

from main import strings
from lib import checks

logs = logging.getLogger('Racu.Core')


class PingCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @bridge.bridge_command(
        name="ping",
        description="Simple status check.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def ping(self, ctx):
        await ctx.respond(content=strings["ping"].format(ctx.author.name))


def setup(client):
    client.add_cog(PingCog(client))
