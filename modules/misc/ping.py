from discord.ext import bridge
from lib.embed_builder import EmbedBuilder
from lib.constants import CONST
from datetime import datetime


async def ping(self, ctx: bridge.BridgeContext) -> None:
    embed = EmbedBuilder.create_success_embed(
        ctx,
        author_text=CONST.STRINGS["ping_author"],
        description=CONST.STRINGS["ping_pong"],
        footer_text=CONST.STRINGS["ping_footer"].format(
            round(1000 * self.client.latency),
        ),
    )
    await ctx.respond(embed=embed)


async def uptime(self, ctx: bridge.BridgeContext, start_time: datetime) -> None:
    unix_timestamp: int = int(round(self.start_time.timestamp()))

    embed = EmbedBuilder.create_success_embed(
        ctx,
        author_text=CONST.STRINGS["ping_author"],
        description=CONST.STRINGS["ping_uptime"].format(unix_timestamp),
        footer_text=CONST.STRINGS["ping_footer"].format(
            round(1000 * self.client.latency),
        ),
    )
    await ctx.respond(embed=embed)
