import os
import platform

import discord
import psutil
from discord.ext import commands

import lib.format
from lib.const import CONST
from ui.embeds import Builder


class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.info.usage = lib.format.generate_usage(self.info)

    @commands.hybrid_command(
        name="info",
    )
    async def info(self, ctx: commands.Context[commands.Bot]) -> None:
        memory_usage_in_mb: float = psutil.Process().memory_info().rss / (1024 * 1024)
        # total_rows: str = Currency.format(BlackJackStats.get_total_rows_count())

        description: str = "".join(
            [
                CONST.STRINGS["info_latency"].format(round(1000 * self.bot.latency)),
                CONST.STRINGS["info_memory"].format(memory_usage_in_mb),
                CONST.STRINGS["info_system"].format(platform.system(), os.name),
                CONST.STRINGS["info_api_version"].format(discord.__version__),
                # CONST.STRINGS["info_database_records"].format(total_rows),
            ],
        )

        embed: discord.Embed = Builder.create_embed(
            theme="info",
            user_name=ctx.author.name,
            author_text=f"{CONST.TITLE} v{CONST.VERSION}",
            author_url=CONST.REPO_URL,
            description=description,
            footer_text=CONST.STRINGS["info_service_footer"],
            thumbnail_url=CONST.LUMI_LOGO_OPAQUE,
            hide_name_in_description=True,
        )

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Info(bot))
