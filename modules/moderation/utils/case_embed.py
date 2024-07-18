import discord
from lib.embed_builder import EmbedBuilder
from lib.constants import CONST
from typing import Optional


def create_case_embed(
    ctx,
    target: discord.User,
    case_number: int,
    action_type: str,
    reason: Optional[str],
) -> discord.Embed:
    embed = EmbedBuilder.create_warning_embed(
        ctx,
        author_text=CONST.STRINGS["case_new_case_author"],
        thumbnail_url=target.display_avatar.url,
        show_name=False,
    )
    embed.add_field(
        name=CONST.STRINGS["case_case_field"],
        value=CONST.STRINGS["case_case_field_value"].format(case_number),
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
