import datetime
from typing import Any

import discord
from discord.ext import commands

from lib.const import CONST
from lib.format import format_case_number, format_seconds_to_duration_string
from ui.embeds import Builder


def create_case_embed(
    ctx: commands.Context[commands.Bot],
    target: discord.User,
    case_number: int,
    action_type: str,
    reason: str | None,
    timestamp: datetime.datetime | None = None,
    duration: int | None = None,
) -> discord.Embed:
    embed: discord.Embed = Builder.create_embed(
        theme="info",
        user_name=ctx.author.name,
        author_text=CONST.STRINGS["case_new_case_author"],
        thumbnail_url=target.display_avatar.url,
        hide_name_in_description=True,
        timestamp=timestamp,
    )

    embed.add_field(
        name=CONST.STRINGS["case_case_field"],
        value=CONST.STRINGS["case_case_field_value"].format(
            format_case_number(case_number),
        ),
        inline=True,
    )

    if not duration:
        embed.add_field(
            name=CONST.STRINGS["case_type_field"],
            value=CONST.STRINGS["case_type_field_value"].format(
                action_type.lower().capitalize(),
            ),
            inline=True,
        )
    else:
        embed.add_field(
            name=CONST.STRINGS["case_type_field"],
            value=CONST.STRINGS["case_type_field_value_with_duration"].format(
                action_type.lower().capitalize(),
                format_seconds_to_duration_string(duration),
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


def create_case_list_embed(
    ctx: commands.Context[commands.Bot],
    cases: list[dict[str, Any]],
    author_text: str,
) -> discord.Embed:
    embed: discord.Embed = Builder.create_embed(
        theme="info",
        user_name=ctx.author.name,
        author_text=author_text,
        hide_name_in_description=True,
    )

    for case in cases:
        status_emoji = "❌" if case.get("is_closed") else "✅"
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
