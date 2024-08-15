from discord.ext import bridge, pages
from lib.constants import CONST
from lib.embed_builder import EmbedBuilder
from lib.embeds.triggers import create_no_triggers_embed
from services.reactions_service import CustomReactionsService
from typing import Any, Dict, List

import discord


async def list_reactions(ctx: bridge.Context) -> None:
    if ctx.guild is None:
        return

    reaction_service: CustomReactionsService = CustomReactionsService()
    guild_id: int = ctx.guild.id

    reactions: List[Dict[str, Any]] = await reaction_service.find_all_by_guild(guild_id)
    if not reactions:
        embed: discord.Embed = create_no_triggers_embed()
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

        embed.description = "\n".join(
            [
                CONST.STRINGS["triggers_list_trigger_text"].format(
                    reaction["trigger_text"],
                ),
                CONST.STRINGS["triggers_list_reaction_type"].format(
                    "Emoji" if reaction["is_emoji"] else "Text",
                ),
                CONST.STRINGS["triggers_list_emoji_id"].format(reaction["emoji_id"])
                if reaction["is_emoji"]
                else CONST.STRINGS["triggers_list_response"].format(
                    reaction["response"],
                ),
                CONST.STRINGS["triggers_list_full_match"].format(
                    reaction["is_full_match"],
                ),
                CONST.STRINGS["triggers_list_usage_count"].format(
                    reaction["usage_count"],
                ),
            ],
        )
        pages_list.append(embed)

    paginator: pages.Paginator = pages.Paginator(pages=pages_list, timeout=180.0)
    await paginator.respond(ctx, ephemeral=False)
