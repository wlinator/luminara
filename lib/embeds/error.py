import discord
from lib import formatter

question_icon = "https://i.imgur.com/8xccUws.png"
exclam_icon = "https://i.imgur.com/vitwMUu.png"


def clean_error_embed(ctx):
    embed = discord.Embed(
        color=discord.Color.red(),
        description=f"**{ctx.author.name}** "
    )

    return embed


class EconErrors:
    @staticmethod
    def missing_bet(ctx):
        """
        See MissingRequiredArgument
        """
        embed = clean_error_embed(ctx)
        embed.description += "please enter a bet."
        embed.set_footer(text=f"For more info do '{formatter.get_prefix(ctx)}help {formatter.get_invoked_name(ctx)}'",
                         icon_url=question_icon)
        return embed

    @staticmethod
    def bad_bet_argument(ctx):
        """
        See BadArgument
        """
        embed = clean_error_embed(ctx)
        embed.description += "the bet you entered is invalid."
        embed.set_footer(text=f"For more info do '{formatter.get_prefix(ctx)}help {formatter.get_invoked_name(ctx)}'",
                         icon_url=question_icon)
        return embed

    @staticmethod
    def bad_argument(ctx):
        """
        See BadArgument
        """
        embed = clean_error_embed(ctx)
        embed.description += "the argument you entered is invalid."
        embed.set_footer(text=f"For more info do '{formatter.get_prefix(ctx)}help {formatter.get_invoked_name(ctx)}'",
                         icon_url=question_icon)
        return embed

    @staticmethod
    def insufficient_balance(ctx):
        embed = clean_error_embed(ctx)
        embed.description += "you don't have enough cash."
        embed.set_footer(text=f"Do '{formatter.get_prefix(ctx)}balance' to see how much you can spend",
                         icon_url=question_icon)
        return embed

    @staticmethod
    def daily_already_claimed(ctx, unix_time):
        embed = clean_error_embed(ctx)
        embed.description += f"already claimed. You can claim your reward again <t:{unix_time}:R>."
        embed.set_footer(text=f"For more info do '{formatter.get_prefix(ctx)}help {formatter.get_invoked_name(ctx)}'",
                         icon_url=question_icon)

        return embed

    @staticmethod
    def out_of_time(ctx):
        embed = clean_error_embed(ctx)
        embed.description += "you ran out of time."
        embed.set_footer(text="Your bet was forfeited", icon_url=exclam_icon)

        return embed

    @staticmethod
    def already_playing(ctx):
        embed = clean_error_embed(ctx)
        embed.description += f"you already have a game of {ctx.command.name} running."
        embed.set_footer(text="Please finish this game first", icon_url=exclam_icon)

        return embed

    @staticmethod
    def generic_exception(ctx):
        embed = clean_error_embed(ctx)
        embed.description += "something went wrong."
        embed.set_footer(text="Try the command again", icon_url=exclam_icon)

        return embed
