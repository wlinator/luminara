import discord

from lib import formatter
from services.Xp import Xp


def welcome_message(member, template=None):

    embed = discord.Embed(
        color=discord.Color.embed_background(),
        description=f"_ _\n**Welcome** to **{member.guild.name}**"
    )

    if template:
        embed.description += "↓↓↓\n" + formatter.template(template, member.name)

    embed.set_thumbnail(url=member.display_avatar)

    return embed


def simple_question_5(question):
    embed = discord.Embed(color=0xadcca6,
                          title=question)

    embed.set_footer(text="max. 5 characters")
    return embed


def simple_question_30(question):
    embed = discord.Embed(color=0xadcca6,
                          title=question)

    embed.set_footer(text="max. 30 characters")
    return embed


def simple_question_100(question):
    embed = discord.Embed(color=0xadcca6,
                          title=question)

    embed.set_footer(text="max. 100 characters")
    return embed


def simple_question_300(question):
    embed = discord.Embed(color=0xadcca6,
                          title=question)

    embed.set_footer(text="max. 300 characters")
    return embed


def simple_question_none(question):
    embed = discord.Embed(color=0xadcca6,
                          title=question)
    return embed


def simple_question_first(question):
    embed = discord.Embed(color=0xadcca6,
                          title=f"You chose to go with the short introduction! "
                                f"Let's start with your nickname. {question}")
    embed.set_footer(text="max. 100 characters")
    return embed


def simple_question_first_extended(question):
    embed = discord.Embed(color=0xadcca6,
                          title=f"You chose to go with the extended introduction! "
                                f"Let's start with your nickname. {question}")
    embed.set_footer(text="max. 100 characters")
    return embed


def no_time():
    embed = discord.Embed(description="You ran out of time or clicked the \"Stop\" button. "
                                      "If you wish to start over, do **/intro**.")
    return embed


def final_embed_short(ctx, nickname, age, location, pronouns, likes, dislikes):
    embed = discord.Embed(color=0x2200FF, description=
    f"**(Nick)name:** {nickname}\n\n**Age:** {age}\n\n"
    f"**Region:** {location}\n\n**Pronouns:** {pronouns}\n\n"
    f"**Likes & interests:** {likes}\n\n**Dislikes:** {dislikes}")

    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.set_footer(text="Type: Short Introduction")

    return embed


def final_embed_extended(ctx, nickname, age, location, languages, pronouns,
                         sexuality, relationship_status, likes, dislikes, extra):
    embed = discord.Embed(color=0xD91E1E, description=
    f"**(Nick)name:** {nickname}\n\n**Age:** {age}\n\n"
    f"**Region:** {location}\n\n**Languages:** {languages}\n\n"
    f"**Pronouns:** {pronouns}\n\n**Sexuality** {sexuality}\n\n"
    f"**Relationship status:** {relationship_status}\n\n**Likes & interests:** {likes}\n\n"
    f"**Dislikes:** {dislikes}\n\n**EXTRAS:** {extra}")

    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.set_footer(text="Type: Extended Introduction")

    return embed


def final_confirmation(channel_id):
    embed = discord.Embed(color=0xadcca6,
                          title="Your introduction has been posted in the server!",
                          description=f"<#{channel_id}>")

    return embed
