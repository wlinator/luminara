import asyncio
import discord

from lib import formatter
from lib.constants import CONST
from lib.embed_builder import EmbedBuilder
from modules.moderation.utils import actionable
from modules.moderation.utils.case_handler import create_case
from typing import Optional


async def ban_user(cog, ctx, target: discord.User, reason: Optional[str] = None):
    # see if user is in guild
    member = await cog.client.get_or_fetch_member(ctx.guild, target.id)

    output_reason = reason or CONST.STRINGS["mod_no_reason"]

    # member -> user is in the guild, check role hierarchy
    if member:
        bot_member = await cog.client.get_or_fetch_member(ctx.guild, ctx.bot.user.id)
        actionable.actionable(member, ctx.author, bot_member)

        try:
            await member.send(
                embed=EmbedBuilder.create_warning_embed(
                    ctx,
                    author_text=CONST.STRINGS["mod_banned_author"],
                    description=CONST.STRINGS["mod_ban_dm"].format(
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

        await member.ban(
            reason=CONST.STRINGS["mod_reason"].format(
                ctx.author.name,
                formatter.shorten(output_reason, 200),
            ),
        )

        respond_task = ctx.respond(
            embed=EmbedBuilder.create_success_embed(
                ctx,
                author_text=CONST.STRINGS["mod_banned_author"],
                description=CONST.STRINGS["mod_banned_user"].format(target.id),
                footer_text=CONST.STRINGS["mod_dm_sent"]
                if dm_sent
                else CONST.STRINGS["mod_dm_not_sent"],
            ),
        )
        create_case_task = create_case(ctx, target, "BAN", reason)
        await asyncio.gather(respond_task, create_case_task, return_exceptions=True)

    # not a member in this guild, so ban right away
    else:
        await ctx.guild.ban(
            target,
            reason=CONST.STRINGS["mod_reason"].format(
                ctx.author.name,
                formatter.shorten(output_reason, 200),
            ),
        )

        respond_task = ctx.respond(
            embed=EmbedBuilder.create_success_embed(
                ctx,
                author_text=CONST.STRINGS["mod_banned_author"],
                description=CONST.STRINGS["mod_banned_user"].format(target.id),
            ),
        )
        create_case_task = create_case(ctx, target, "BAN", reason)
        await asyncio.gather(respond_task, create_case_task)


async def unban_user(ctx, target: discord.User, reason: Optional[str] = None):
    output_reason = reason or CONST.STRINGS["mod_no_reason"]

    try:
        await ctx.guild.unban(
            target,
            reason=CONST.STRINGS["mod_reason"].format(
                ctx.author.name,
                formatter.shorten(output_reason, 200),
            ),
        )

        respond_task = ctx.respond(
            embed=EmbedBuilder.create_success_embed(
                ctx,
                author_text=CONST.STRINGS["mod_unbanned_author"],
                description=CONST.STRINGS["mod_unbanned"].format(target.id),
            ),
        )
        create_case_task = create_case(ctx, target, "UNBAN", reason)
        await asyncio.gather(respond_task, create_case_task)

    except (discord.NotFound, discord.HTTPException):
        return await ctx.respond(
            embed=EmbedBuilder.create_warning_embed(
                ctx,
                author_text=CONST.STRINGS["mod_not_banned_author"],
                description=CONST.STRINGS["mod_not_banned"].format(target.id),
            ),
        )
