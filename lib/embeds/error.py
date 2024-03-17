import discord
from lib import formatter

question_icon = "https://i.imgur.com/8xccUws.png"


def clean_error_embed():
    embed = discord.Embed(
        color=discord.Color.red()
    )

    return embed


class EconErrors:
    @staticmethod
    def missing_bet(ctx):
        """
        See MissingRequiredArgument
        """
        embed = clean_error_embed()
        embed.description = f"**{ctx.author.name}** please enter a bet."
        embed.set_footer(text=f"For more info do '{formatter.get_prefix(ctx)}help {formatter.get_invoked_name(ctx)}'",
                         icon_url=question_icon)
        return embed

    @staticmethod
    def bad_bet_argument(ctx):
        """
        See BadArgument
        """
        embed = clean_error_embed()
        embed.description = f"**{ctx.author.name}** the bet you entered is invalid."
        embed.set_footer(text=f"For more info do '{formatter.get_prefix(ctx)}help {formatter.get_invoked_name(ctx)}'",
                         icon_url=question_icon)
        return embed

    @staticmethod
    def insufficient_balance(ctx):
        embed = clean_error_embed()
        embed.description = f"**{ctx.author.name}** you don't have enough cash."
        embed.set_footer(text=f"Do '{formatter.get_prefix(ctx)}balance' to see how much you can spend",
                         icon_url=question_icon)
        return embed

    @staticmethod
    def daily_already_claimed(ctx, unix_time):
        embed = clean_error_embed()
        embed.description = f"**{ctx.author.name}** already claimed. You can claim your reward again <t:{unix_time}:R>."
        embed.set_footer(text=f"For more info do '{formatter.get_prefix(ctx)}help {formatter.get_invoked_name(ctx)}'",
                         icon_url=question_icon)

        return embed
