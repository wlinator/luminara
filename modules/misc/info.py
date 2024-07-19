import os
import platform

import discord
import psutil
from discord.ext import bridge

from lib.constants import CONST
from lib.embed_builder import EmbedBuilder
from services.currency_service import Currency
from services.stats_service import BlackJackStats


async def cmd(self, ctx: bridge.Context, unix_timestamp: int) -> None:
    memory_usage_in_mb: float = psutil.Process().memory_info().rss / (1024 * 1024)
    total_rows: str = Currency.format(BlackJackStats.get_total_rows_count())

    description: str = "".join(
        [
            CONST.STRINGS["info_uptime"].format(unix_timestamp),
            CONST.STRINGS["info_latency"].format(round(1000 * self.client.latency)),
            CONST.STRINGS["info_memory"].format(memory_usage_in_mb),
            CONST.STRINGS["info_system"].format(platform.system(), os.name),
            CONST.STRINGS["info_api_version"].format(discord.__version__),
            CONST.STRINGS["info_database_records"].format(total_rows),
        ],
    )

    embed: discord.Embed = EmbedBuilder.create_success_embed(
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

    await ctx.respond(embed=embed)
