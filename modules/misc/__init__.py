import logging

import discord
from discord.ext import commands, bridge
import datetime, time
from lib.embeds.info import MiscInfo

from lib import checks
from main import strings

logs = logging.getLogger('Racu.Core')


class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.start_time = datetime.datetime.now()

    @bridge.bridge_command(
        name="ping",
        aliases=["p", "status"],
        description="Simple status check.",
        help="Simple status check, this command will not return the latency of the bot process as this is "
             "fairly irrelevant. If the bot replies, it's good to go.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def ping(self, ctx):
        return await ctx.respond(embed=MiscInfo.ping(ctx, self.client))

    @bridge.bridge_command(
        name="uptime",
        description="Racu uptime",
        help="See how long Racu has been online, the uptime shown will reset when the Misc module is reloaded.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def uptime(self, ctx):

        unix_timestamp = int(round(self.start_time.timestamp()))
        return await ctx.respond(embed=MiscInfo.uptime(ctx, self.client, unix_timestamp))


def setup(client):
    client.add_cog(Misc(client))
