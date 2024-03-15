import discord
from discord.ext import commands

from services.Xp import Xp
from lib import embeds, checks


class LevelCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        name="level",
        description="Displays your level and server rank.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def level(self, ctx):
        xp_data = Xp(ctx.author.id, ctx.guild.id)
        rank = xp_data.calculate_rank()
        needed_xp_for_next_level = Xp.xp_needed_for_next_level(xp_data.level)

        embed = discord.Embed(color=0xadcca6,
                              title=f"Level {xp_data.level}")
        embed.add_field(name=f"Progress to next level",
                        value=Xp.generate_progress_bar(xp_data.xp, needed_xp_for_next_level), inline=False)

        embed.set_footer(text=f"Server Rank: #{rank}")
        embed.set_thumbnail(url=ctx.author.display_avatar)

        await ctx.respond(embed=embed, content=ctx.author.mention)


def setup(client):
    client.add_cog(LevelCog(client))
