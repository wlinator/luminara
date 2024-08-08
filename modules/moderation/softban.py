import asyncio
import discord
from typing import Optional
from discord.ext.commands import MemberConverter, UserConverter
from lib import formatter
from lib.constants import CONST
from lib.embed_builder import EmbedBuilder
from modules.moderation.utils.actionable import async_actionable
from modules.moderation.utils.case_handler import create_case


async def softban_user(ctx, target: discord.Member, reason: Optional[str] = None):
    bot_member = await MemberConverter().convert(ctx, str(ctx.bot.user.id))
    await async_actionable(target, ctx.author, bot_member)

    output_reason = reason or CONST.STRINGS["mod_no_reason"]

    try:
        await target.send(
            embed=EmbedBuilder.create_warning_embed(
                ctx,
                author_text=CONST.STRINGS["mod_softbanned_author"],
                description=CONST.STRINGS["mod_softban_dm"].format(
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

    await ctx.guild.ban(
        target,
        reason=CONST.STRINGS["mod_reason"].format(
            ctx.author.name,
            formatter.shorten(output_reason, 200),
        ),
        delete_message_seconds=86400,
    )

    await ctx.guild.unban(
        target,
        reason=CONST.STRINGS["mod_softban_unban_reason"].format(
            ctx.author.name,
        ),
    )

    respond_task = ctx.respond(
        embed=EmbedBuilder.create_success_embed(
            ctx,
            author_text=CONST.STRINGS["mod_softbanned_author"],
            description=CONST.STRINGS["mod_softbanned_user"].format(target.name),
            footer_text=CONST.STRINGS["mod_dm_sent"]
            if dm_sent
            else CONST.STRINGS["mod_dm_not_sent"],
        ),
    )

    target_user = await UserConverter().convert(ctx, str(target.id))
    create_case_task = create_case(ctx, target_user, "SOFTBAN", reason)
    await asyncio.gather(respond_task, create_case_task, return_exceptions=True)
