import asyncio
from typing import Optional

import discord
from discord.ext.commands import UserConverter, MemberConverter

from lib import formatter
from lib.constants import CONST
from lib.embed_builder import EmbedBuilder
from modules.moderation.utils.actionable import async_actionable
from modules.moderation.utils.case_handler import create_case


async def kick_user(cog, ctx, target: discord.Member, reason: Optional[str] = None):
    bot_member = await MemberConverter().convert(ctx, str(ctx.bot.user.id))
    await async_actionable(target, ctx.author, bot_member)

    output_reason = reason or CONST.STRINGS["mod_no_reason"]

    try:
        await target.send(
            embed=EmbedBuilder.create_warning_embed(
                ctx,
                author_text=CONST.STRINGS["mod_kicked_author"],
                description=CONST.STRINGS["mod_kick_dm"].format(
                    target.name,
                    ctx.guild.name,
                    output_reason,
                ),
                show_name=False,
            ),
        )
        dm_sent = True

    except (discord.HTTPException, discord.Forbidden):
        dm_sent = False

    await target.kick(
        reason=CONST.STRINGS["mod_reason"].format(
            ctx.author.name,
            formatter.shorten(output_reason, 200),
        ),
    )

    respond_task = ctx.respond(
        embed=EmbedBuilder.create_success_embed(
            ctx,
            author_text=CONST.STRINGS["mod_kicked_author"],
            description=CONST.STRINGS["mod_kicked_user"].format(target.name),
            footer_text=CONST.STRINGS["mod_dm_sent"]
            if dm_sent
            else CONST.STRINGS["mod_dm_not_sent"],
        ),
    )

    target_user = await UserConverter().convert(ctx, str(target.id))
    create_case_task = create_case(ctx, target_user, "KICK", reason)
    await asyncio.gather(respond_task, create_case_task, return_exceptions=True)
