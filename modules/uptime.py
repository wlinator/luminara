from discord.ext import commands
import datetime, time
from main import strings
from sb_tools import universal


class UptimeCog(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot
        self.start_time = time.time()

    @commands.slash_command(
        name="uptime",
        description="Simple status check.",
        guild_only=True
    )
    @commands.check(universal.channel_check)
    async def uptime(self, ctx):
        current_time = time.time()

        difference = int(round(current_time - self.start_time))

        text = str(datetime.timedelta(seconds=difference))
        await ctx.send(content=strings["uptime"].format(ctx.author.name, text))


def setup(sbbot):
    sbbot.add_cog(UptimeCog(sbbot))
