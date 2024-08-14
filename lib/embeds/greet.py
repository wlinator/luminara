import discord
from lib import formatter


class Greet:
    @staticmethod
    def message(member, template=None):
        embed = discord.Embed(
            color=discord.Color.embed_background(),
            description=f"_ _\n**Welcome** to **{member.guild.name}**",
        )
        if template:
            embed.description = (
                f"{embed.description}\n↓↓↓\n{formatter.template(template, member.name)}"
            )

        embed.set_thumbnail(url=member.display_avatar.url)

        return embed
