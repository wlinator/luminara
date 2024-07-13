import discord

from lib.constants import CONST


def clean_intro_embed(ctx):
    embed = discord.Embed(
        color=discord.Color.blurple(), description=f"**{ctx.author.name}** "
    )

    return embed





class General:
    @staticmethod
    def post_confirmation(ctx, channel):
        embed = clean_intro_embed(ctx)
        embed.description = (embed.description or "") + f" your introduction has been posted in {channel.mention}!"  # Added space for proper concatenation

        return embed
