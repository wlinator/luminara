import discord

from config.parser import JsonCache

resources = JsonCache.read_json("art")

question_icon = resources["icons"]["question"]
exclaim_icon = resources["icons"]["exclaim"]


def clean_intro_embed(ctx):
    embed = discord.Embed(
        color=discord.Color.blurple(),
        description=f"**{ctx.author.name}** "
    )

    return embed


class Questions:
    @staticmethod
    def question(ctx, text):
        embed = clean_intro_embed(ctx)
        embed.description += text
        embed.set_footer(text="Type your answer below", icon_url=exclaim_icon)

        return embed


class General:
    @staticmethod
    def start(ctx, channel):
        embed = clean_intro_embed(ctx)
        embed.description += (f"this command will serve as a questionnaire for your entry to {channel.mention}. "
                              f"Please keep your answers \"PG-13\" and don't abuse this command.")
        embed.set_footer(text="Click the button below to start", icon_url=exclaim_icon)

        return embed

    @staticmethod
    def clicked_stop(ctx):
        embed = clean_intro_embed(ctx)
        embed.description += "the introduction command was stopped."

        return embed

    @staticmethod
    def preview(ctx, answer_mapping: dict):
        embed = discord.Embed(color=discord.Color.embed_background(), description="")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)

        for key, answer in answer_mapping.items():
            embed.description += f"**{key}:** {answer}\n\n"

        return embed

    @staticmethod
    def post_confirmation(ctx, channel):
        embed = clean_intro_embed(ctx)
        embed.description += f"your introduction has been posted in {channel.mention}!"

        return embed
