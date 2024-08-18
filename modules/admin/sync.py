import discord

from lib.constants import CONST
from lib.embed_builder import EmbedBuilder
from lib.exceptions.LumiExceptions import LumiException


async def sync_commands(client, ctx):
    try:
        await client.sync_commands()
        embed = EmbedBuilder.create_success_embed(
            ctx,
            author_text=CONST.STRINGS["admin_sync_title"],
            description=CONST.STRINGS["admin_sync_description"],
        )
        await ctx.send(embed=embed)
    except discord.HTTPException as e:
        raise LumiException(
            CONST.STRINGS["admin_sync_error_description"].format(e),
        ) from e
