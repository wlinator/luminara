from typing import Optional

from discord.ext import bridge

from lib import formatter
from lib.constants import CONST
from lib.embed_builder import EmbedBuilder
from lib.exceptions.LumiExceptions import LumiException
from services.reactions_service import CustomReactionsService


async def add_reaction(
        ctx: bridge.Context,
        trigger_text: str,
        response: Optional[str],
        emoji_id: Optional[int],
        is_emoji: bool,
        is_full_match: bool,
) -> None:
    if ctx.guild is None:
        return

    reaction_service = CustomReactionsService()
    guild_id: int = ctx.guild.id
    creator_id: int = ctx.author.id

    if not await check_reaction_limit(
            reaction_service,
            guild_id,
    ):
        return

    if not await check_existing_trigger(
            reaction_service,
            guild_id,
            trigger_text,
    ):
        return

    success: bool = await reaction_service.create_custom_reaction(
        guild_id=guild_id,
        creator_id=creator_id,
        trigger_text=trigger_text,
        response=response,
        emoji_id=emoji_id,
        is_emoji=is_emoji,
        is_full_match=is_full_match,
        is_global=False,
    )

    if not success:
        raise LumiException(CONST.STRINGS["triggers_not_added"])

    trigger_text = formatter.shorten(trigger_text, 50)

    if response:
        response = formatter.shorten(response, 50)

    embed = EmbedBuilder.create_success_embed(
        ctx,
        author_text=CONST.STRINGS["triggers_add_author"],
        description="",
        footer_text=CONST.STRINGS["triggers_reaction_service_footer"],
        show_name=False,
    )

    embed.description += CONST.STRINGS["triggers_add_description"].format(
        trigger_text,
        CONST.STRINGS["triggers_type_emoji"]
        if is_emoji
        else CONST.STRINGS["triggers_type_text"],
        is_full_match,
    )

    if is_emoji:
        embed.description += CONST.STRINGS["triggers_add_emoji_details"].format(
            emoji_id,
        )
    else:
        embed.description += CONST.STRINGS["triggers_add_text_details"].format(response)

    await ctx.respond(embed=embed)


async def check_reaction_limit(
        reaction_service: CustomReactionsService,
        guild_id: int,
) -> bool:
    limit_reached = await reaction_service.count_custom_reactions(guild_id) >= 100

    if limit_reached:
        raise LumiException(CONST.STRINGS["trigger_limit_reached"])

    return True


async def check_existing_trigger(
        reaction_service: CustomReactionsService,
        guild_id: int,
        trigger_text: str,
) -> bool:
    existing_trigger = await reaction_service.find_trigger(guild_id, trigger_text)

    if existing_trigger:
        raise LumiException(CONST.STRINGS["trigger_already_exists"])

    return True
