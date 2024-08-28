from typing import Optional
from discord.ext import commands
from discord import Embed, Guild
from lib.const import CONST
from ui.embeds import builder
from ui.views.leaderboard import LeaderboardCommandOptions, LeaderboardCommandView


class Leaderboard(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.hybrid_command(
        name="leaderboard",
        aliases=["lb"],
        usage="leaderboard",
    )
    async def leaderboard(self, ctx: commands.Context[commands.Bot]) -> None:
        guild: Optional[Guild] = ctx.guild
        if not guild:
            return

        options: LeaderboardCommandOptions = LeaderboardCommandOptions()
        view: LeaderboardCommandView = LeaderboardCommandView(ctx, options)

        embed: Embed = builder.create_embed(
            theme="info",
            user_name=ctx.author.name,
            thumbnail_url=ctx.author.display_avatar.url,
            hide_name_in_description=True,
        )

        icon: str = guild.icon.url if guild.icon else CONST.FLOWERS_ART
        await view.populate_leaderboard("xp", embed, icon)

        await ctx.send(embed=embed, view=view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Leaderboard(bot))
