from datetime import datetime
from enum import Enum

import discord

from lib.const import CONST


class Theme(Enum):
    ERROR = "error"
    SUCCESS = "success"
    INFO = "info"
    WARNING = "warning"
    DEFAULT = "default"


class Builder:
    ERROR = Theme.ERROR
    SUCCESS = Theme.SUCCESS
    INFO = Theme.INFO
    WARNING = Theme.WARNING
    DEFAULT = Theme.DEFAULT

    @staticmethod
    def create_embed(
        theme: Theme,
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
            Theme.ERROR: (CONST.COLOR_ERROR, CONST.CROSS_ICON),
            Theme.SUCCESS: (CONST.COLOR_DEFAULT, CONST.CHECK_ICON),
            Theme.INFO: (CONST.COLOR_DEFAULT, CONST.INFO_ICON),
            Theme.WARNING: (CONST.COLOR_WARNING, CONST.WARNING_ICON),
            Theme.DEFAULT: (color or CONST.COLOR_DEFAULT, None),
        }

        embed_color, theme_icon = theme_settings[theme]

        if user_name and not hide_name_in_description:
            description = f"**{user_name}** {description or ''}"

        embed = discord.Embed(
            title=title,
            description=description,
            color=embed_color,
            timestamp=None if hide_time else (timestamp or discord.utils.utcnow()),
        )

        embed.set_author(
            name=author_text or user_name,
            icon_url=author_icon_url or theme_icon or user_display_avatar_url,
            url=author_url,
        )

        embed.set_footer(text=footer_text or CONST.TITLE, icon_url=footer_icon_url or CONST.LUMI_LOGO_TRANSPARENT)

        if image_url:
            embed.set_image(url=image_url)
        if thumbnail_url:
            embed.set_thumbnail(url=thumbnail_url)

        return embed
