import discord

from data.Xp import Xp


def command_error_1():
    embed = discord.Embed(
        color=discord.Color.red(),
        description="I'm not even sure how you reached this error but here we are. Try the command again."
    )
    embed.set_footer(text="And tell Tess!!!")

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


#
# def level_up_message(level, rank):
#     embed = discord.Embed(color=0xadcca6,
#                           title=f"You reached level {level}!")
#     embed.set_footer(text=f"Rank: #{rank} | Leaderboard coming soon")
#     return embed


def level_command_message(ctx, level, xp, next_level_xp, rank):
    embed = discord.Embed(color=0xadcca6,
                          title=f"{ctx.author.name} - lv. {level}")
    embed.add_field(name="Progress to Next Level", value=Xp.generate_progress_bar(xp, next_level_xp), inline=False)
    embed.set_footer(text=f"The Rave Cave | Server Rank: #{rank}")
    embed.set_thumbnail(url=ctx.author.avatar.url)
    return embed


async def leaderboard_message(ctx, leaderboard):
    embed = discord.Embed(
        color=0xadcca6
    )
    embed.set_author(name="Rave Cave Leaderboard",
                     icon_url="https://cdn.discordapp.com/icons/719227135151046699/"
                              "49df8c284382af9dbcfd629c8eadc52c.webp?size=96")
    embed.set_footer(text=f"Do /level to see your rank.")
    embed.set_thumbnail(url="https://i.imgur.com/79XfsbS.png")
    for i, (user_id, xp, level, rank, xp_needed_for_next_level) in enumerate(leaderboard[:5], start=1):
        member = await ctx.guild.fetch_member(user_id)
        embed.add_field(
            name=f"#{rank} - {member.name}",
            value=f"level: `{level}`\nxp: `{xp}/{xp_needed_for_next_level}`",
            inline=False
        )

    return embed
