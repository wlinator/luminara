import asyncio
import discord
from discord.ext.commands import UserConverter
from services.moderation.case_service import CaseService
from modules.moderation.utils.case_embed import (
    create_case_embed,
    create_case_list_embed,
)
from lib.embed_builder import EmbedBuilder
from lib.constants import CONST
from discord.ext import pages
from lib.formatter import format_case_number
from modules.moderation.utils.case_handler import edit_case_modlog

case_service = CaseService()


async def view_case_by_number(ctx, guild_id: int, case_number: int):
    case = case_service.fetch_case_by_guild_and_number(guild_id, case_number)

    if not case:
        embed = EmbedBuilder.create_error_embed(
            ctx,
            author_text=CONST.STRINGS["error_no_case_found_author"],
            description=CONST.STRINGS["error_no_case_found_description"],
        )
        return await ctx.respond(embed=embed)

    target = await UserConverter().convert(ctx, str(case["target_id"]))
    embed = create_case_embed(
        ctx,
        target,
        case["case_number"],
        case["action_type"],
        case["reason"],
        case["created_at"],
    )
    await ctx.respond(embed=embed)


async def view_all_cases_in_guild(ctx, guild_id: int):
    cases = case_service.fetch_cases_by_guild(guild_id)

    if not cases:
        embed = EmbedBuilder.create_error_embed(
            ctx,
            author_text=CONST.STRINGS["case_guild_no_cases_author"],
            description=CONST.STRINGS["case_guild_no_cases"],
        )
        return await ctx.respond(embed=embed)

    pages_list = []
    for i in range(0, len(cases), 10):
        chunk = cases[i : i + 10]
        embed = create_case_list_embed(
            ctx,
            chunk,
            CONST.STRINGS["case_guild_cases_author"],
        )
        pages_list.append(embed)

    paginator = pages.Paginator(pages=pages_list)
    await paginator.respond(ctx)


async def view_all_cases_by_mod(ctx, guild_id: int, moderator: discord.User):
    cases = case_service.fetch_cases_by_moderator(guild_id, moderator.id)

    if not cases:
        embed = EmbedBuilder.create_error_embed(
            ctx,
            author_text=CONST.STRINGS["case_mod_no_cases_author"],
            description=CONST.STRINGS["case_mod_no_cases"],
        )
        return await ctx.respond(embed=embed)

    pages_list = []
    for i in range(0, len(cases), 10):
        chunk = cases[i : i + 10]
        embed = create_case_list_embed(
            ctx,
            chunk,
            CONST.STRINGS["case_mod_cases_author"].format(moderator.name),
        )
        pages_list.append(embed)

    paginator = pages.Paginator(pages=pages_list)
    await paginator.respond(ctx)


async def edit_case_reason(ctx, guild_id: int, case_number: int, new_reason: str):
    case_service.edit_case_reason(
        guild_id,
        case_number,
        new_reason,
    )

    embed = EmbedBuilder.create_success_embed(
        ctx,
        author_text=CONST.STRINGS["case_reason_update_author"],
        description=CONST.STRINGS["case_reason_update_description"].format(
            format_case_number(case_number),
        ),
    )

    async def update_tasks():
        await asyncio.gather(
            ctx.respond(embed=embed),
            edit_case_modlog(ctx, guild_id, case_number, new_reason),
        )

    await update_tasks()
