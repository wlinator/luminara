from typing import Optional

import discord
from lib.constants import CONST
from services.blacklist_service import BlacklistUserService
from lib.embed_builder import EmbedBuilder


async def blacklist_user(
    ctx,
    user: discord.User,
    reason: Optional[str] = None,
) -> None:
    blacklist_service = BlacklistUserService(user.id)
    blacklist_service.add_to_blacklist(reason)

    embed = EmbedBuilder.create_success_embed(
        ctx,
        author_text=CONST.STRINGS["admin_blacklist_author"],
        description=CONST.STRINGS["admin_blacklist_description"].format(user.name),
        footer_text=CONST.STRINGS["admin_blacklist_footer"],
        hide_timestamp=True,
    )

    await ctx.send(embed=embed)
