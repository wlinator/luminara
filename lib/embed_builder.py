import discord
from lib.constants import CONST
import datetime


class EmbedBuilder:
    @staticmethod
    def create_embed(
        ctx,
        title=None,
        author_text=None,
        author_icon_url=None,
        author_url=None,
        description=None,
        color=None,
        footer_text=None,
        footer_icon_url=None,
        show_name=True,
        image_url=None,
        thumbnail_url=None,
    ):
        if not author_text:
            author_text = ctx.author.name
        elif show_name:
            description = f"**{ctx.author.name}** {description}"

        if not author_icon_url:
            author_icon_url = ctx.author.display_avatar.url
        if not footer_text:
            footer_text = "Luminara"
        if not footer_icon_url:
            footer_icon_url = CONST.LUMI_LOGO_TRANSPARENT

        embed = discord.Embed(
            title=title,
            description=description,
            color=color or CONST.COLOR_DEFAULT,
        )
        embed.set_author(name=author_text, icon_url=author_icon_url, url=author_url)
        embed.set_footer(text=footer_text, icon_url=footer_icon_url)
        embed.timestamp = datetime.datetime.now()

        if image_url:
            embed.set_image(url=image_url)
        if thumbnail_url:
            embed.set_thumbnail(url=thumbnail_url)

        return embed

    @staticmethod
    def create_error_embed(
        ctx,
        title=None,
        author_text=None,
        author_icon_url=None,
        author_url=None,
        description=None,
        footer_text=None,
        show_name=True,
        image_url=None,
        thumbnail_url=None,
    ):
        return EmbedBuilder.create_embed(
            ctx,
            title=title,
            author_text=author_text,
            author_icon_url=author_icon_url or CONST.CROSS_ICON,
            author_url=author_url,
            description=description,
            color=CONST.COLOR_ERROR,
            footer_text=footer_text,
            footer_icon_url=CONST.LUMI_LOGO_TRANSPARENT,
            show_name=show_name,
            image_url=image_url,
            thumbnail_url=thumbnail_url,
        )

    @staticmethod
    def create_success_embed(
        ctx,
        title=None,
        author_text=None,
        author_icon_url=None,
        author_url=None,
        description=None,
        footer_text=None,
        show_name=True,
        image_url=None,
        thumbnail_url=None,
    ):
        return EmbedBuilder.create_embed(
            ctx,
            title=title,
            author_text=author_text,
            author_icon_url=author_icon_url or CONST.CHECK_ICON,
            author_url=author_url,
            description=description,
            color=CONST.COLOR_DEFAULT,
            footer_text=footer_text,
            footer_icon_url=CONST.LUMI_LOGO_TRANSPARENT,
            show_name=show_name,
            image_url=image_url,
            thumbnail_url=thumbnail_url,
        )

    @staticmethod
    def create_info_embed(
        ctx,
        title=None,
        author_text=None,
        author_icon_url=None,
        author_url=None,
        description=None,
        footer_text=None,
        show_name=True,
        image_url=None,
        thumbnail_url=None,
    ):
        return EmbedBuilder.create_embed(
            ctx,
            title=title,
            author_text=author_text,
            author_icon_url=author_icon_url or CONST.EXCLAIM_ICON,
            author_url=author_url,
            description=description,
            color=CONST.COLOR_DEFAULT,
            footer_text=footer_text,
            footer_icon_url=CONST.LUMI_LOGO_TRANSPARENT,
            show_name=show_name,
            image_url=image_url,
            thumbnail_url=thumbnail_url,
        )

    @staticmethod
    def create_warning_embed(
        ctx,
        title=None,
        author_text=None,
        author_icon_url=None,
        author_url=None,
        description=None,
        footer_text=None,
        show_name=True,
        image_url=None,
        thumbnail_url=None,
    ):
        return EmbedBuilder.create_embed(
            ctx,
            title=title,
            author_text=author_text,
            author_icon_url=author_icon_url or CONST.WARNING_ICON,
            author_url=author_url,
            description=description,
            color=CONST.COLOR_WARNING,
            footer_text=footer_text,
            footer_icon_url=CONST.LUMI_LOGO_TRANSPARENT,
            show_name=show_name,
            image_url=image_url,
            thumbnail_url=thumbnail_url,
        )
