from datetime import datetime

import discord
from discord import Embed
from discord.ext import commands

from lib.const import CONST
from ui.embeds import Builder


class Uptime(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.start_time: datetime = discord.utils.utcnow()

    @commands.hybrid_command(
        name="uptime",
        usage="uptime",
    )
    async def uptime(self, ctx: commands.Context[commands.Bot]) -> None:
        unix_timestamp: int = int(self.start_time.timestamp())

        embed: Embed = Builder.create_embed(
            theme="info",
            user_name=ctx.author.name,
            author_text=CONST.STRINGS["ping_author"],
            description=CONST.STRINGS["ping_uptime"].format(unix_timestamp),
            footer_text=CONST.STRINGS["ping_footer"].format(
                int(self.bot.latency * 1000),
            ),
        )
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Uptime(bot))
