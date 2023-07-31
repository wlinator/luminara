import logging

import discord
from discord.ext import commands

from sb_tools import universal

racu_logs = logging.getLogger('Racu.Core')


class SayCog(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot

    @commands.slash_command(
        name="tess",
        description="Bot admin only",
        guild_only=True
    )
    @commands.check(universal.owner_check)
    async def tess_command(self, ctx, *, txt: discord.Option(str)):
        await ctx.respond(content="✅", ephemeral=True)
        await ctx.send(content=txt)


def setup(sbbot):
    sbbot.add_cog(SayCog(sbbot))
