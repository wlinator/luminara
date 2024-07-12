import discord

from lib.constants import CONST


def clean_intro_embed(ctx):
    embed = discord.Embed(
        color=discord.Color.blurple(), description=f"**{ctx.author.name}** "
    )

    return embed


class Questions:
    @staticmethod
    def question(ctx, text):
        embed = clean_intro_embed(ctx)
        embed.description += text
        embed.set_footer(text="Type your answer below", icon_url=CONST.EXCLAIM_ICON)

        return embed


class General:
    @staticmethod
    def start(ctx, channel):
        embed = clean_intro_embed(ctx)
        embed.description = (
            (embed.description or "")
            + f"this command will serve as a questionnaire for your entry to {channel.mention}. "
            f'Please keep your answers "PG-13" and don\'t abuse this command.'
        )
        embed.set_footer(text="Click the button below to start", icon_url=CONST.EXCLAIM_ICON)

        return embed

    @staticmethod
    def clicked_stop(ctx):
        embed = clean_intro_embed(ctx)
        embed.description = (
            embed.description or ""
        ) + " the introduction command was stopped."
        return embed

    @staticmethod
    def preview(ctx, answer_mapping: dict):
        embed = discord.Embed(
            color=discord.Color.blurple(), description=""
        )  # Corrected color
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        description = ""

        for key, answer in answer_mapping.items():
            description += f"**{key}:** {answer}\n\n"

        embed.description = description
        return embed

    @staticmethod
    def post_confirmation(ctx, channel):
        embed = clean_intro_embed(ctx)
        embed.description = (embed.description or "") + f" your introduction has been posted in {channel.mention}!"  # Added space for proper concatenation

        return embed
