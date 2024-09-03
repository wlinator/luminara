from datetime import datetime

import discord
from discord import Embed
from discord.ext import commands

import lib.format
from lib.client import Luminara
from lib.const import CONST
from ui.embeds import Builder


class Uptime(commands.Cog):
    def __init__(self, bot: Luminara) -> None:
        self.bot: Luminara = bot
        self.start_time: datetime = discord.utils.utcnow()
        self.uptime.usage = lib.format.generate_usage(self.uptime)

    @commands.hybrid_command(name="uptime")
    async def uptime(self, ctx: commands.Context[Luminara]) -> None:
        """
        Uptime command.

        Parameters
        ----------
        ctx : commands.Context[Luminara]
            The context of the command.
        """
        unix_timestamp: int = int(self.start_time.timestamp())

        embed: Embed = Builder.create_embed(
            Builder.INFO,
            user_name=ctx.author.name,
            author_text=CONST.STRINGS["ping_author"],
            description=CONST.STRINGS["ping_uptime"].format(unix_timestamp),
            footer_text=CONST.STRINGS["ping_footer"].format(
                int(self.bot.latency * 1000),
            ),
        )
        await ctx.send(embed=embed)


async def setup(bot: Luminara) -> None:
    await bot.add_cog(Uptime(bot))
