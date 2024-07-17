from discord.ext import bridge
from typing import Optional
from services.reactions_service import CustomReactionsService
from lib.embeds.triggers import create_creation_embed, create_failure_embed


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
        ctx,
        reaction_service,
        guild_id,
        trigger_text,
        is_emoji,
    ):
        return

    if not await check_existing_trigger(
        ctx,
        reaction_service,
        guild_id,
        trigger_text,
        is_emoji,
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
        is_global=False,  # only bot admins can create global custom reactions
    )

    if success:
        embed = create_creation_embed(
            trigger_text,
            response,
            emoji_id,
            is_emoji,
            is_full_match,
        )
        await ctx.respond(embed=embed)
    else:
        embed = create_failure_embed(trigger_text, is_emoji)
        await ctx.respond(embed=embed)


async def check_reaction_limit(
    ctx: bridge.Context,
    reaction_service: CustomReactionsService,
    guild_id: int,
    trigger_text: str,
    is_emoji: bool,
) -> bool:
    if await reaction_service.count_custom_reactions(guild_id) >= 100:
        embed = create_failure_embed(trigger_text, is_emoji, limit_reached=True)
        await ctx.respond(embed=embed)
        return False
    return True


async def check_existing_trigger(
    ctx: bridge.Context,
    reaction_service: CustomReactionsService,
    guild_id: int,
    trigger_text: str,
    is_emoji: bool,
) -> bool:
    existing_trigger = await reaction_service.find_trigger(guild_id, trigger_text)
    if existing_trigger:
        embed = create_failure_embed(
            trigger_text,
            is_emoji,
            trigger_already_exists=True,
        )
        await ctx.respond(embed=embed)
        return False
    return True
