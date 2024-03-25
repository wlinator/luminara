import discord

from config.parser import JsonCache
from lib import formatter

resources = JsonCache.read_json("resources")

question_icon = resources["icons"]["racu_question"]
exclam_icon = resources["icons"]["racu_exclam"]


class Greet:
    @staticmethod
    def message(member, template=None):

        embed = discord.Embed(
            color=discord.Color.embed_background(),
            description=f"_ _\n**Welcome** to **{member.guild.name}**"
        )

        if template:
            embed.description += "↓↓↓\n" + formatter.template(template, member.name)

        embed.set_thumbnail(url=member.display_avatar)

        return embed

