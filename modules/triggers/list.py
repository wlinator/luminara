from typing import Any, Dict, List

import discord
from discord.ext import bridge, pages

from lib import formatter
from lib.constants import CONST
from lib.embed_builder import EmbedBuilder
from services.reactions_service import CustomReactionsService


async def list_reactions(ctx: bridge.Context) -> None:
    if ctx.guild is None:
        return

    reaction_service: CustomReactionsService = CustomReactionsService()
    guild_id: int = ctx.guild.id

    reactions: List[Dict[str, Any]] = await reaction_service.find_all_by_guild(guild_id)
    if not reactions:
        embed: discord.Embed = EmbedBuilder.create_warning_embed(
            ctx,
            author_text=CONST.STRINGS["triggers_no_reactions_title"],
            description=CONST.STRINGS["triggers_no_reactions_description"],
            footer_text=CONST.STRINGS["triggers_reaction_service_footer"],
            show_name=False,
        )
        await ctx.respond(embed=embed)
        return

    pages_list = []
    for reaction in reactions:
        embed = EmbedBuilder.create_success_embed(
            ctx,
            title=CONST.STRINGS["triggers_list_custom_reaction_id"].format(
                reaction["id"],
            ),
            author_text=CONST.STRINGS["triggers_list_custom_reactions_title"],
            footer_text=CONST.STRINGS["triggers_reaction_service_footer"],
            show_name=False,
        )

        description_lines = [
            CONST.STRINGS["triggers_list_trigger_text"].format(
                formatter.shorten(reaction["trigger_text"], 50),
            ),
            CONST.STRINGS["triggers_list_reaction_type"].format(
                CONST.STRINGS["triggers_type_emoji"]
                if reaction["is_emoji"]
                else CONST.STRINGS["triggers_type_text"],
            ),
        ]

        if reaction["is_emoji"]:
            description_lines.append(
                CONST.STRINGS["triggers_list_emoji_id"].format(reaction["emoji_id"]),
            )
        else:
            description_lines.append(
                CONST.STRINGS["triggers_list_response"].format(
                    formatter.shorten(reaction["response"], 50),
                ),
            )

        description_lines.extend(
            [
                CONST.STRINGS["triggers_list_full_match"].format(
                    "True" if reaction["is_full_match"] else "False",
                ),
                CONST.STRINGS["triggers_list_usage_count"].format(
                    reaction["usage_count"],
                ),
            ],
        )

        embed.description = "\n".join(description_lines)
        pages_list.append(embed)

    paginator: pages.Paginator = pages.Paginator(pages=pages_list, timeout=180.0)
    await paginator.respond(ctx, ephemeral=False)
