import discord

from lib.constants import CONST


def clean_error_embed(ctx):
    return discord.Embed(
        color=discord.Color.red(),
        description=f"**{ctx.author.name}** ",
    )


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
