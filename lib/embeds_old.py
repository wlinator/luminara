import discord

from lib import formatter


def welcome_message(member, template=None):

    embed = discord.Embed(
        color=discord.Color.embed_background(),
        description=f"_ _\n**Welcome** to **{member.guild.name}**"
    )

    if template:
        embed.description += "↓↓↓\n" + formatter.template(template, member.name)

    embed.set_thumbnail(url=member.display_avatar)

    return embed
