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
        description=None,
        color=None,
        footer_text=None,
        footer_icon_url=None,
        show_name=True,
    ):
        if not author_text:
            author_text = ctx.author.name
        elif show_name:
            description = f"**{ctx.author.name}** {description}"

        if not author_icon_url:
            author_icon_url = ctx.author.avatar.url
        if not footer_text:
            footer_text = "Luminara"
        if not footer_icon_url:
            footer_icon_url = CONST.LUMI_LOGO_TRANSPARENT

        embed = discord.Embed(
            title=title,
            description=description,
            color=color or CONST.COLOR_DEFAULT,
        )
        embed.set_author(name=author_text, icon_url=author_icon_url)

        embed.set_footer(text=footer_text, icon_url=footer_icon_url)
        embed.timestamp = datetime.datetime.now()

        return embed

    @staticmethod
    def create_error_embed(
        ctx,
        title=None,
        author_text=None,
        description=None,
        footer_text=None,
        show_name=True,
    ):
        return EmbedBuilder.create_embed(
            ctx,
            title=title,
            author_text=author_text,
            author_icon_url=CONST.CROSS_ICON,
            description=description,
            color=CONST.COLOR_ERROR,
            footer_text=footer_text,
            footer_icon_url=CONST.LUMI_LOGO_TRANSPARENT,
            show_name=show_name,
        )

    @staticmethod
    def create_success_embed(
        ctx,
        title=None,
        author_text=None,
        description=None,
        footer_text=None,
        show_name=True,
    ):
        return EmbedBuilder.create_embed(
            ctx,
            title=title,
            author_text=author_text,
            author_icon_url=CONST.CHECK_ICON,
            description=description,
            color=CONST.COLOR_DEFAULT,
            footer_text=footer_text,
            footer_icon_url=CONST.LUMI_LOGO_TRANSPARENT,
            show_name=show_name,
        )

    @staticmethod
    def create_info_embed(
        ctx,
        title=None,
        author_text=None,
        description=None,
        footer_text=None,
        show_name=True,
    ):
        return EmbedBuilder.create_embed(
            ctx,
            title=title,
            author_text=author_text,
            author_icon_url=CONST.EXCLAIM_ICON,
            description=description,
            color=CONST.COLOR_DEFAULT,
            footer_text=footer_text,
            footer_icon_url=CONST.LUMI_LOGO_TRANSPARENT,
            show_name=show_name,
        )

    @staticmethod
    def create_warning_embed(
        ctx,
        title=None,
        author_text=None,
        description=None,
        footer_text=None,
        show_name=True,
    ):
        return EmbedBuilder.create_embed(
            ctx,
            title=title,
            author_text=author_text,
            author_icon_url=CONST.WARNING_ICON,
            description=description,
            color=CONST.COLOR_WARNING,
            footer_text=footer_text,
            footer_icon_url=CONST.LUMI_LOGO_TRANSPARENT,
            show_name=show_name,
        )
