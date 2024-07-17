from discord.ext import bridge

from lib.embeds.triggers import (
    create_deletion_embed,
    create_failure_embed,
    create_not_found_embed,
)
from services.reactions_service import CustomReactionsService


async def delete_reaction(ctx: bridge.Context, reaction_id: int) -> None:
    if ctx.guild is None:
        return

    reaction_service = CustomReactionsService()
    guild_id: int = ctx.guild.id

    # Check if the reaction exists and belongs to the guild
    reaction = await reaction_service.find_id(reaction_id)
    if reaction is None or reaction["guild_id"] != guild_id or reaction["is_global"]:
        embed = create_not_found_embed(reaction_id)
        await ctx.respond(embed=embed)
        return

    trigger_text = reaction["trigger_text"]
    is_emoji = reaction["is_emoji"]

    # Attempt to delete the reaction
    success: bool = await reaction_service.delete_custom_reaction(reaction_id)

    if success:
        embed = create_deletion_embed(trigger_text, is_emoji)
        await ctx.respond(embed=embed)
    else:
        embed = create_failure_embed(trigger_text, is_emoji)
        await ctx.respond(embed=embed)
