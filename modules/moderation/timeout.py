import asyncio
import discord
import datetime

from lib import formatter
from lib.constants import CONST
from lib.embed_builder import EmbedBuilder
from modules.moderation.utils.actionable import async_actionable
from modules.moderation.utils.case_handler import create_case
from typing import Optional
from discord.ext.commands import UserConverter
from lib.formatter import format_duration_to_seconds, format_seconds_to_duration_string


async def timeout_user(
    cog,
    ctx,
    target: discord.Member,
    duration: str,
    reason: Optional[str] = None,
):
    bot_member = await cog.client.get_or_fetch_member(ctx.guild, ctx.bot.user.id)
    await async_actionable(target, ctx.author, bot_member)

    output_reason = reason or CONST.STRINGS["mod_no_reason"]

    # Parse duration to minutes and validate
    duration_int = format_duration_to_seconds(duration)
    duration_str = format_seconds_to_duration_string(duration_int)

    await target.timeout_for(
        duration=datetime.timedelta(seconds=duration_int),
        reason=CONST.STRINGS["mod_reason"].format(
            ctx.author.name,
            formatter.shorten(output_reason, 200),
        ),
    )

    dm_task = target.send(
        embed=EmbedBuilder.create_warning_embed(
            ctx,
            author_text=CONST.STRINGS["mod_timed_out_author"],
            description=CONST.STRINGS["mod_timeout_dm"].format(
                target.name,
                ctx.guild.name,
                duration_str,
                output_reason,
            ),
            show_name=False,
        ),
    )

    respond_task = ctx.respond(
        embed=EmbedBuilder.create_success_embed(
            ctx,
            author_text=CONST.STRINGS["mod_timed_out_author"],
            description=CONST.STRINGS["mod_timed_out_user"].format(target.name),
        ),
    )

    target_user = await UserConverter().convert(ctx, str(target.id))
    create_case_task = create_case(ctx, target_user, "TIMEOUT", reason, duration_int)

    await asyncio.gather(
        dm_task,
        respond_task,
        create_case_task,
        return_exceptions=True,
    )


async def untimeout_user(ctx, target: discord.Member, reason: Optional[str] = None):
    output_reason = reason or CONST.STRINGS["mod_no_reason"]

    try:
        await target.remove_timeout(
            reason=CONST.STRINGS["mod_reason"].format(
                ctx.author.name,
                formatter.shorten(output_reason, 200),
            ),
        )

        respond_task = ctx.respond(
            embed=EmbedBuilder.create_success_embed(
                ctx,
                author_text=CONST.STRINGS["mod_untimed_out_author"],
                description=CONST.STRINGS["mod_untimed_out"].format(target.name),
            ),
        )

        target_user = await UserConverter().convert(ctx, str(target.id))
        create_case_task = create_case(ctx, target_user, "UNTIMEOUT", reason)
        await asyncio.gather(respond_task, create_case_task)

    except discord.HTTPException:
        return await ctx.respond(
            embed=EmbedBuilder.create_warning_embed(
                ctx,
                author_text=CONST.STRINGS["mod_not_timed_out_author"],
                description=CONST.STRINGS["mod_not_timed_out"].format(target.name),
            ),
        )
