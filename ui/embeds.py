from datetime import datetime
from typing import Optional, Literal

import discord

from lib.const import CONST


class builder:
    @staticmethod
    def create_embed(
        user_name: Optional[str] = None,
        user_display_avatar_url: Optional[str] = None,
        theme: Optional[Literal["error", "success", "info", "warning"]] = None,
        title: Optional[str] = None,
        author_text: Optional[str] = None,
        author_icon_url: Optional[str] = None,
        author_url: Optional[str] = None,
        description: Optional[str] = None,
        color: Optional[int] = None,
        footer_text: Optional[str] = None,
        footer_icon_url: Optional[str] = None,
        image_url: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        timestamp: Optional[datetime] = None,
        hide_name_in_description: bool = False,
        hide_time: bool = False,
    ) -> discord.Embed:
        """
        Create a standard Lumi embed with the given parameters.
        """

        theme_settings = {
            "error": (CONST.COLOR_ERROR, CONST.CROSS_ICON),
            "success": (CONST.COLOR_DEFAULT, CONST.CHECK_ICON),
            "info": (CONST.COLOR_DEFAULT, CONST.INFO_ICON),
            "warning": (CONST.COLOR_WARNING, CONST.WARNING_ICON),
        }
        if theme in theme_settings:
            color, author_icon_url = theme_settings[theme]

        if user_name and not hide_name_in_description:
            description = f"**{user_name}** {description}"

        embed: discord.Embed = discord.Embed(
            title=title,
            description=description,
            color=color or CONST.COLOR_DEFAULT,
        )

        embed.set_author(
            name=author_text or user_name or None,
            icon_url=author_icon_url or user_display_avatar_url or None,
            url=author_url,
        )

        embed.set_footer(
            text=footer_text or CONST.TITLE,
            icon_url=footer_icon_url or CONST.LUMI_LOGO_TRANSPARENT,
        )

        embed.timestamp = None if hide_time else (timestamp or datetime.now())
        if image_url:
            embed.set_image(url=image_url)
        if thumbnail_url:
            embed.set_thumbnail(url=thumbnail_url)

        return embed
