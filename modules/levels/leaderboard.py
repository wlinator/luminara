from typing import cast

from discord import Embed, Guild, Member
from discord.ext import commands

from lib.const import CONST
from ui.embeds import Builder
from ui.views.leaderboard import LeaderboardCommandOptions, LeaderboardCommandView


class Leaderboard(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.hybrid_command(
        name="leaderboard",
        aliases=["lb"],
    )
    async def leaderboard(self, ctx: commands.Context[commands.Bot]) -> None:
        """
        Get the leaderboard for the server.

        Parameters
        ----------
        ctx : commands.Context[commands.Bot]
            The context of the command.
        """
        guild: Guild | None = ctx.guild
        if not guild:
            return

        options: LeaderboardCommandOptions = LeaderboardCommandOptions()
        view: LeaderboardCommandView = LeaderboardCommandView(ctx, options)

        author: Member = cast(Member, ctx.author)
        embed: Embed = Builder.create_embed(
            theme="info",
            user_name=author.name,
            thumbnail_url=author.display_avatar.url,
            hide_name_in_description=True,
        )

        icon: str = guild.icon.url if guild.icon else CONST.FLOWERS_ART
        await view.populate_leaderboard("xp", embed, icon)

        await ctx.send(embed=embed, view=view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Leaderboard(bot))
