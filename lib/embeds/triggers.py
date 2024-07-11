import discord
from typing import Optional
from config.parser import JsonCache
from lib import formatter
import datetime

resources = JsonCache.read_json("art")

check_icon = resources["icons"]["check"]
cross_icon = resources["icons"]["cross"]
logo = resources["logo"]["transparent"]

def create_embed(title: str, description: str, color: int, icon_url: str) -> discord.Embed:
    embed = discord.Embed(
        color=color,
        description=description
    )
    embed.set_author(name=title, icon_url=icon_url)
    embed.set_footer(text="Reaction Service", icon_url=logo)
    embed.timestamp = datetime.datetime.utcnow()
    return embed


def create_creation_embed(trigger_text: str, response: Optional[str], emoji_id: Optional[int], is_emoji: bool, is_full_match: bool) -> discord.Embed:
    trigger_text = formatter.shorten(trigger_text, 50)
    if response:
        response = formatter.shorten(response, 50)
    
    description = (
        f"**Trigger Text:** `{trigger_text}`\n"
        f"**Reaction Type:** {'Emoji' if is_emoji else 'Text'}\n"
        f"{f'**Emoji ID:** `{str(emoji_id)}`' if is_emoji else f'**Response:** `{response}`'}\n"
               f"**Full Match:** `{is_full_match}`"
    )
    return create_embed("Custom Reaction Created", description, 0xFF8C00, check_icon)

def create_failure_embed(trigger_text: str, is_emoji: bool, limit_reached: bool = False, trigger_already_exists: bool = False) -> discord.Embed:
    trigger_text = formatter.shorten(trigger_text, 50)
    
    description = f"**Trigger Text:** `{trigger_text}`\n"
    
    if limit_reached:
        description += "Failed to add custom reaction. You have reached the limit of 100 custom reactions for this server."
    elif trigger_already_exists:
        description += "Failed to add custom reaction. This text already contains another trigger. To avoid unexpected behavior, please delete it before adding a new one."
    else:
        description += "Failed to add custom reaction."

    return create_embed("Custom Reaction Creation Failed", description, 0xFF0000, cross_icon)