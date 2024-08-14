import datetime

import discord
from discord.ext import bridge, pages
from lib.constants import CONST
from lib.embeds.triggers import create_no_triggers_embed
from services.reactions_service import CustomReactionsService


async def list_reactions(ctx: bridge.Context) -> None:
    if ctx.guild is None:
        return

    reaction_service = CustomReactionsService()
    guild_id: int = ctx.guild.id

    # Fetch all reactions for the guild
    reactions = await reaction_service.find_all_by_guild(guild_id)
    if not reactions:
        embed = create_no_triggers_embed()
        await ctx.respond(embed=embed)
        return

    # Create pages for pagination
    pages_list = []
    for reaction in reactions:
        description = f"""**Trigger Text:** `{reaction['trigger_text']}`\n**Reaction Type:** {'Emoji' if reaction['is_emoji'] else 'Text'}\n{f"**Emoji ID:** `{str(reaction['emoji_id'])}`" if reaction['is_emoji'] else f"**Response:** `{reaction['response']}`"}\n**Full Match:** `{'True' if reaction['is_full_match'] else 'False'}`\n**Usage Count:** `{reaction['usage_count']}`"""
        embed = discord.Embed(
            title=f"ID: {reaction['id']}",
            description=description,
            color=0xFF8C00,
        )
        embed.set_author(name="Custom Reactions", icon_url=CONST.CHECK_ICON)
        embed.set_footer(text="Reaction Service", icon_url=CONST.LUMI_LOGO_TRANSPARENT)
        embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
        pages_list.append(embed)

    paginator = pages.Paginator(pages=pages_list, timeout=180.0)
    await paginator.respond(ctx, ephemeral=False)
