import discord
from lib.embed_builder import EmbedBuilder
from lib.constants import CONST
from lib.formatter import format_case_number
from typing import Optional
import datetime


def create_case_embed(
    ctx,
    target: discord.User,
    case_number: int,
    action_type: str,
    reason: Optional[str],
    timestamp: Optional[datetime.datetime] = None,
) -> discord.Embed:
    embed = EmbedBuilder.create_warning_embed(
        ctx,
        author_text=CONST.STRINGS["case_new_case_author"],
        thumbnail_url=target.display_avatar.url,
        show_name=False,
        timestamp=timestamp,
    )
    embed.add_field(
        name=CONST.STRINGS["case_case_field"],
        value=CONST.STRINGS["case_case_field_value"].format(
            format_case_number(case_number),
        ),
        inline=True,
    )
    embed.add_field(
        name=CONST.STRINGS["case_type_field"],
        value=CONST.STRINGS["case_type_field_value"].format(
            action_type.lower().capitalize(),
        ),
        inline=True,
    )
    embed.add_field(
        name=CONST.STRINGS["case_moderator_field"],
        value=CONST.STRINGS["case_moderator_field_value"].format(
            ctx.author.name,
        ),
        inline=True,
    )
    embed.add_field(
        name=CONST.STRINGS["case_target_field"],
        value=CONST.STRINGS["case_target_field_value"].format(target.name),
        inline=False,
    )
    embed.add_field(
        name=CONST.STRINGS["case_reason_field"],
        value=CONST.STRINGS["case_reason_field_value"].format(
            reason or CONST.STRINGS["mod_no_reason"],
        ),
        inline=False,
    )
    return embed


def create_case_list_embed(ctx, cases: list, author_text: str) -> discord.Embed:
    embed = EmbedBuilder.create_success_embed(
        ctx,
        author_text=author_text,
        show_name=False,
    )

    for case in cases:
        status_emoji = "✅" if not case.get("is_closed") else "❌"
        case_number = case.get("case_number", "N/A")

        if isinstance(case_number, int):
            case_number = format_case_number(case_number)

        action_type = case.get("action_type", "Unknown")
        timestamp = case.get("created_at", "Unknown")

        if isinstance(timestamp, datetime.datetime):
            formatted_timestamp = f"<t:{int(timestamp.timestamp())}:R>"
        else:
            formatted_timestamp = str(timestamp)

        if embed.description is None:
            embed.description = ""
        embed.description += f"{status_emoji} `{case_number}` **[{action_type}]** {formatted_timestamp}\n"

    return embed
