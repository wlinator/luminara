import discord

from lib import formatter
from lib.constants import CONST


def clean_error_embed(ctx):
    return discord.Embed(
        color=discord.Color.red(),
        description=f"**{ctx.author.name}** ",
    )


class GenericErrors:
    @staticmethod
    def bad_arg(ctx, error):
        embed = clean_error_embed(ctx)
        if embed.description is None:
            embed.description = formatter.shorten(str(error), 100)
        else:
            embed.description += formatter.shorten(str(error), 100)
        embed.set_footer(
            text=f"For more info do {formatter.get_prefix(ctx)}help {formatter.get_invoked_name(ctx)}",
            icon_url=CONST.QUESTION_ICON,
        )

        return embed

    @staticmethod
    def private_message_only(ctx):
        embed = clean_error_embed(ctx)
        if embed.description is None:
            embed.description = "this command can only be used in private messages."
        else:
            embed.description += "this command can only be used in private messages."
        embed.set_footer(
            text=f"For more info do '{formatter.get_prefix(ctx)}help {formatter.get_invoked_name(ctx)}'",
            icon_url=CONST.QUESTION_ICON,
        )

        return embed

    @staticmethod
    def guild_only(ctx):
        embed = clean_error_embed(ctx)
        if embed.description is None:
            embed.description = "this command can only be used in a server."
        else:
            embed.description += "this command can only be used in a server."
        embed.set_footer(
            text=f"For more info do '{formatter.get_prefix(ctx)}help {formatter.get_invoked_name(ctx)}'",
            icon_url=CONST.QUESTION_ICON,
        )

        return embed

    @staticmethod
    def channel_not_allowed(ctx, channel):
        embed = clean_error_embed(ctx)
        if embed.description is None:
            embed.description = f"you can only do that command in {channel.mention}."
        else:
            embed.description += f"you can only do that command in {channel.mention}."
        embed.set_footer(
            text="This message will delete itself after 5s",
            icon_url=CONST.EXCLAIM_ICON,
        )

        return embed


class EconErrors:
    @staticmethod
    def out_of_time(ctx):
        embed = clean_error_embed(ctx)
        if embed.description is None:
            embed.description = "you ran out of time."
        else:
            embed.description += "you ran out of time."
        embed.set_footer(text="Your bet was forfeited", icon_url=CONST.EXCLAIM_ICON)

        return embed

    @staticmethod
    def already_playing(ctx):
        embed = clean_error_embed(ctx)
        if embed.description is None:
            embed.description = (
                f"you already have a game of {ctx.command.name} running."
            )
        else:
            embed.description += (
                f"you already have a game of {ctx.command.name} running."
            )
        embed.set_footer(
            text="Please finish this game first",
            icon_url=CONST.EXCLAIM_ICON,
        )

        return embed


class MiscErrors:
    @staticmethod
    def prefix_too_long(ctx):
        embed = clean_error_embed(ctx)
        if embed.description is None:
            embed.description = "this prefix is too long."
        else:
            embed.description += "this prefix is too long."
        embed.set_footer(
            text=f"For more info do '{formatter.get_prefix(ctx)}help {formatter.get_invoked_name(ctx)}'",
            icon_url=CONST.QUESTION_ICON,
        )

        return embed


class HelpErrors:
    @staticmethod
    def error_message(ctx, error):
        """
        See discord.ext.commands.HelpCommand.send_error_message
        """
        embed = clean_error_embed(ctx)
        embed.description += error
        embed.set_footer(
            text=f"See '{formatter.get_prefix(ctx)}help'",
            icon_url=CONST.EXCLAIM_ICON,
        )

        return embed
