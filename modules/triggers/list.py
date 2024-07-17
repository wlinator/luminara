import discord
from discord.ext import bridge, pages
from services.reactions_service import CustomReactionsService
from lib.embeds.triggers import create_no_triggers_embed
from config.parser import JsonCache
import datetime

resources = JsonCache.read_json("art")

check_icon = resources["icons"]["check"]
logo = resources["logo"]["transparent"]


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
        description = (
            f"**Trigger Text:** `{reaction['trigger_text']}`\n"
            f"**Reaction Type:** {'Emoji' if reaction['is_emoji'] else 'Text'}\n"
            f"{'**Emoji ID:** `{}`'.format(str(reaction['emoji_id'])) if reaction['is_emoji'] else '**Response:** `{}`'.format(reaction['response'])}\n"
            f"**Full Match:** `{'True' if reaction['is_full_match'] else 'False'}`\n"
            f"**Usage Count:** `{reaction['usage_count']}`"
        )
        embed = discord.Embed(
            title=f"ID: {reaction['id']}",
            description=description,
            color=0xFF8C00,
        )
        embed.set_author(name="Custom Reactions", icon_url=check_icon)
        embed.set_footer(text="Reaction Service", icon_url=logo)
        embed.timestamp = datetime.datetime.utcnow()
        pages_list.append(embed)

    paginator = pages.Paginator(pages=pages_list, timeout=180.0)
    await paginator.respond(ctx, ephemeral=False)
