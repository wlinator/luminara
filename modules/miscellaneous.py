import logging

from discord.ext import commands, bridge
import datetime, time

from main import strings
from lib import checks

logs = logging.getLogger('Racu.Core')


class Miscellaneous(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.start_time = time.time()

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
        await ctx.respond(content=strings["ping"].format(ctx.author.name))

    @bridge.bridge_command(
        name="uptime",
        description="Racu uptime",
        help="See how long Racu has been online, the uptime shown will reset when the Misc module is reloaded.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def uptime(self, ctx):
        current_time = time.time()

        difference = int(round(current_time - self.start_time))

        text = str(datetime.timedelta(seconds=difference))
        await ctx.respond(content=strings["uptime"].format(ctx.author.name, text))


def setup(client):
    client.add_cog(Miscellaneous(client))
