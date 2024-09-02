from datetime import datetime
from typing import Literal

import discord

from lib.const import CONST


class Builder:
    @staticmethod
    def create_embed(
        theme: Literal["error", "success", "info", "warning", "default"],
        user_name: str | None = None,
        user_display_avatar_url: str | None = None,
        title: str | None = None,
        author_text: str | None = None,
        author_icon_url: str | None = None,
        author_url: str | None = None,
        description: str | None = None,
        color: int | None = None,
        footer_text: str | None = None,
        footer_icon_url: str | None = None,
        image_url: str | None = None,
        thumbnail_url: str | None = None,
        timestamp: datetime | None = None,
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
            "default": (color or CONST.COLOR_DEFAULT, None),
        }

        color, author_icon_url = theme_settings[theme]

        if user_name and not hide_name_in_description:
            description = f"**{user_name}** {description}"

        embed: discord.Embed = discord.Embed(
            title=title,
            description=description,
            color=color,
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

        embed.timestamp = None if hide_time else (timestamp or discord.utils.utcnow())
        if image_url:
            embed.set_image(url=image_url)
        if thumbnail_url:
            embed.set_thumbnail(url=thumbnail_url)

        return embed
