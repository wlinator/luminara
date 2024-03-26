import logging
import os
import platform

import discord
import psutil

from config.parser import JsonCache
from lib import metadata
from services.BlackJackStats import BlackJackStats
from services.Currency import Currency

_logs = logging.getLogger('Racu.Core')
_data = JsonCache.read_json("resources")


async def cmd(command, ctx, unix_timestamp):
    memory_usage = psutil.Process().memory_info().rss
    memory_usage_in_mb = memory_usage / (1024 * 1024)

    total_rows = BlackJackStats.get_total_rows_count()
    total_rows = Currency.format(total_rows)

    embed = discord.Embed(
        color=discord.Color.orange()
    )
    embed.set_author(name=f"{metadata.__title__} v{metadata.__version__}",
                     url=_data["gitlab_url"],
                     icon_url=_data["icons"]["racu_logo_transparent"])
    embed.set_thumbnail(url=_data["icons"]["racu_logo"])

    embed.add_field(name="Author", value=f"[{metadata.__author__}]({_data['author_url']})", inline=False)
    embed.add_field(name="Uptime", value=f"<t:{unix_timestamp}:R>")
    embed.add_field(name="Latency", value=f"{round(1000 * command.client.latency)}ms")
    embed.add_field(name="Memory", value=f"{memory_usage_in_mb:.2f} MB")
    embed.add_field(name="System", value=f"{platform.system()} ({os.name})")
    embed.add_field(name="API", value=f"v{discord.__version__}")
    embed.add_field(name="Database", value=f"{total_rows} records")

    return await ctx.respond(embed=embed)
