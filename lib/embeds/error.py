import discord

from config.parser import JsonCache
from lib import formatter

resources = JsonCache.read_json("art")

question_icon = resources["icons"]["question"]
exclaim_icon = resources["icons"]["exclaim"]


def clean_error_embed(ctx):
    embed = discord.Embed(
        color=discord.Color.red(), description=f"**{ctx.author.name}** "
    )

    return embed


class GenericErrors:
    @staticmethod
    def default_exception(ctx):
        embed = clean_error_embed(ctx)
        embed.description += "something went wrong."

        return embed

    @staticmethod
    def bad_arg(ctx, error):
        embed = clean_error_embed(ctx)
        embed.description += formatter.shorten(str(error), 100)
        embed.set_footer(
            text=f"For more info do {formatter.get_prefix(ctx)}help {formatter.get_invoked_name(ctx)}",
            icon_url=question_icon,
        )

        return embed

    @staticmethod
    def bad_url(ctx, error="the image URL must end with `.jpg` or `.png`."):
        embed = clean_error_embed(ctx)
        embed.description += formatter.shorten(str(error), 100)

        return embed

    @staticmethod
    def missing_permissions(ctx):
        embed = clean_error_embed(ctx)
        embed.description += "you are missing permissions to run this command."
        embed.set_footer(
            text=f"For more info do '{formatter.get_prefix(ctx)}help {formatter.get_invoked_name(ctx)}'",
            icon_url=question_icon,
        )

        return embed

    @staticmethod
    def bot_missing_permissions(ctx):
        embed = clean_error_embed(ctx)
        embed.description += "I can't perform this command because I don't have the required permissions."
        embed.set_footer(
            text=f"For more info do '{formatter.get_prefix(ctx)}help {formatter.get_invoked_name(ctx)}'",
            icon_url=question_icon,
        )

        return embed

    @staticmethod
    def command_on_cooldown(ctx, cooldown):
        embed = clean_error_embed(ctx)
        embed.description += "you are on cooldown."
        embed.set_footer(text=f"Try again in {cooldown}", icon_url=exclaim_icon)

        return embed

    @staticmethod
    def owner_only(ctx):
        embed = clean_error_embed(ctx)
        embed.description += "this command requires Lumi ownership permissions."

        return embed

    @staticmethod
    def private_message_only(ctx):
        embed = clean_error_embed(ctx)
        embed.description += f"this command can only be used in private messages."
        embed.set_footer(
            text=f"For more info do '{formatter.get_prefix(ctx)}help {formatter.get_invoked_name(ctx)}'",
            icon_url=question_icon,
        )

        return embed

    @staticmethod
    def guild_only(ctx):
        embed = clean_error_embed(ctx)
        embed.description += f"this command can only be used in a server."
        embed.set_footer(
            text=f"For more info do '{formatter.get_prefix(ctx)}help {formatter.get_invoked_name(ctx)}'",
            icon_url=question_icon,
        )

        return embed

    @staticmethod
    def channel_not_allowed(ctx, channel):
        embed = clean_error_embed(ctx)
        embed.description += f"you can only do that command in {channel.mention}."
        embed.set_footer(
            text="This message will delete itself after 5s", icon_url=exclaim_icon
        )

        return embed


class EconErrors:
    @staticmethod
    def daily_already_claimed(ctx, unix_time):
        embed = clean_error_embed(ctx)
        embed.description += (
            f"already claimed. You can claim your reward again <t:{unix_time}:R>."
        )
        embed.set_footer(
            text=f"For more info do '{formatter.get_prefix(ctx)}help {formatter.get_invoked_name(ctx)}'",
            icon_url=question_icon,
        )

        return embed

    @staticmethod
    def out_of_time(ctx):
        embed = clean_error_embed(ctx)
        embed.description += "you ran out of time."
        embed.set_footer(text="Your bet was forfeited", icon_url=exclaim_icon)

        return embed

    @staticmethod
    def already_playing(ctx):
        embed = clean_error_embed(ctx)
        embed.description += f"you already have a game of {ctx.command.name} running."
        embed.set_footer(text="Please finish this game first", icon_url=exclaim_icon)

        return embed


class BdayErrors:
    @staticmethod
    def birthdays_disabled(ctx):
        embed = clean_error_embed(ctx)
        embed.description += "birthdays are disabled in this server."

        return embed


class MiscErrors:
    @staticmethod
    def prefix_too_long(ctx):
        embed = clean_error_embed(ctx)
        embed.description += "this prefix is too long."
        embed.set_footer(
            text=f"For more info do '{formatter.get_prefix(ctx)}help {formatter.get_invoked_name(ctx)}'",
            icon_url=question_icon,
        )

        return embed

    @staticmethod
    def intro_no_guild(ctx, client_side=False):
        embed = clean_error_embed(ctx)

        if not client_side:
            embed.description += "you're not in a server that supports introductions."
        else:
            embed.description += "I'm not in a server that supports introductions."

        embed.set_footer(
            text="this will be updated soon, stay tuned", icon_url=exclaim_icon
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
            text=f"See '{formatter.get_prefix(ctx)}help'", icon_url=question_icon
        )

        return embed


class IntroErrors:
    @staticmethod
    def timeout(ctx):
        embed = clean_error_embed(ctx)
        embed.description += "you ran out of time to answer this question."
        embed.set_footer(
            text=f"Please do {formatter.get_prefix(ctx)}{formatter.get_invoked_name(ctx)} again",
            icon_url=exclaim_icon,
        )

        return embed

    @staticmethod
    def too_long(ctx):
        embed = clean_error_embed(ctx)
        embed.description += (
            "your answer was too long, please keep it below 200 characters."
        )
        embed.set_footer(
            text=f"Please do {formatter.get_prefix(ctx)}{formatter.get_invoked_name(ctx)} again",
            icon_url=exclaim_icon,
        )

        return embed

    @staticmethod
    def intro_no_channel(ctx):
        embed = clean_error_embed(ctx)
        embed.description += "the introduction channel is missing."
        embed.set_footer(
            text="Please contact a server administrator", icon_url=exclaim_icon
        )

        return embed
