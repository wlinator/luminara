import logging

from discord.ext import commands

from main import strings
from sb_tools import universal

racu_logs = logging.getLogger('Racu.Core')


class PingCog(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot

    @commands.slash_command(
        name="ping",
        description="Simple status check.",
        guild_only=True
    )
    @commands.check(universal.channel_check)
    async def ping(self, ctx):
        await ctx.respond(content=strings["ping"].format(ctx.author.name))


def setup(sbbot):
    sbbot.add_cog(PingCog(sbbot))
