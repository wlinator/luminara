from typing import List, Tuple, Optional

import discord
from discord import Guild

from lib.constants import CONST
from lib.embed_builder import EmbedBuilder
from services.config_service import GuildConfig
from services.moderation.modlog_service import ModLogService


async def cmd(ctx) -> None:
    guild_config: GuildConfig = GuildConfig(ctx.guild.id)
    guild: Guild = ctx.guild
    embed: discord.Embed = EmbedBuilder().create_success_embed(
        ctx=ctx,
        author_text=CONST.STRINGS["config_show_author"].format(guild.name),
        thumbnail_url=guild.icon.url if guild.icon else CONST.LUMI_LOGO_TRANSPARENT,
        show_name=False,
    )

    config_items: List[Tuple[str, bool, bool]] = [
        (
            CONST.STRINGS["config_show_birthdays"],
            bool(guild_config.birthday_channel_id),
            False,
        ),
        (
            CONST.STRINGS["config_show_new_member_greets"],
            bool(guild_config.welcome_channel_id),
            False,
        ),
        (
            CONST.STRINGS["config_show_boost_announcements"],
            bool(guild_config.boost_channel_id),
            False,
        ),
        (
            CONST.STRINGS["config_show_level_announcements"],
            guild_config.level_message_type != 0,
            False,
        ),
    ]

    for name, enabled, default_enabled in config_items:
        status: str = (
            CONST.STRINGS["config_show_enabled"]
            if enabled
            else CONST.STRINGS["config_show_disabled"]
        )
        if not enabled and default_enabled:
            status = CONST.STRINGS["config_show_default_enabled"]
        embed.add_field(name=name, value=status, inline=False)

    modlog_service: ModLogService = ModLogService()
    modlog_channel_id: Optional[int] = modlog_service.fetch_modlog_channel_id(guild.id)
    modlog_channel = guild.get_channel(modlog_channel_id) if modlog_channel_id else None

    modlog_status: str
    if modlog_channel:
        modlog_status = CONST.STRINGS["config_show_moderation_log_enabled"].format(
            modlog_channel.mention,
        )
    elif modlog_channel_id:
        modlog_status = CONST.STRINGS["config_show_moderation_log_channel_deleted"]
    else:
        modlog_status = CONST.STRINGS["config_show_moderation_log_not_configured"]

    embed.add_field(
        name=CONST.STRINGS["config_show_moderation_log"],
        value=modlog_status,
        inline=False,
    )

    await ctx.respond(embed=embed)
