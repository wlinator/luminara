from discord.ext import commands

from services.Xp import Xp
from lib import embeds, checks


class LevelCog(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.slash_command(
        name="level",
        description="Displays your level and rank.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def level(self, ctx):
        xp_data = Xp(ctx.author.id)
        rank = xp_data.calculate_rank()
        needed_xp_for_next_level = Xp.xp_needed_for_next_level(xp_data.level)

        await ctx.respond(embed=embeds.level_command_message(ctx, xp_data.level, xp_data.xp,
                                                             needed_xp_for_next_level, rank))


def setup(client):
    client.add_cog(LevelCog(client))
