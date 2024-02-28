from discord.ext import commands
import datetime, time
from main import strings
from lib import checks


class UptimeCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.start_time = time.time()

    @commands.slash_command(
        name="uptime",
        description="Simple status check.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def uptime(self, ctx):
        current_time = time.time()

        difference = int(round(current_time - self.start_time))

        text = str(datetime.timedelta(seconds=difference))
        await ctx.respond(content=strings["uptime"].format(ctx.author.name, text))


def setup(client):
    client.add_cog(UptimeCog(client))
