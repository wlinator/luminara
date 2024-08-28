from discord.ext import commands
from lib.const import CONST
from ui.embeds import builder
import discord
import os
import platform
import psutil


class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="info",
        usage="info",
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

        embed: discord.Embed = builder.create_success_embed(
            ctx,
            description=description,
            footer_text=CONST.STRINGS["info_service_footer"],
            show_name=False,
        )
        embed.set_author(
            name=f"{CONST.TITLE} v{CONST.VERSION}",
            url=CONST.REPO_URL,
            icon_url=CONST.CHECK_ICON,
        )
        embed.set_thumbnail(url=CONST.LUMI_LOGO_OPAQUE)

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Info(bot))
