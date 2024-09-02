from discord import Embed
from discord.ext import commands

import lib.format
from lib.const import CONST
from services.xp_service import XpService
from ui.embeds import Builder


class Level(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.level.usage = lib.format.generate_usage(self.level)

    @commands.hybrid_command(
        name="level",
        aliases=["rank", "lvl", "xp"],
    )
    async def level(self, ctx: commands.Context[commands.Bot]) -> None:
        """
        Get the level of the user.

        Parameters
        ----------
        ctx : commands.Context[commands.Bot]
            The context of the command.
        """
        if not ctx.guild:
            return

        xp_data: XpService = XpService(ctx.author.id, ctx.guild.id)

        rank: str = str(xp_data.calculate_rank())
        needed_xp_for_next_level: int = XpService.xp_needed_for_next_level(
            xp_data.level,
        )

        embed: Embed = Builder.create_embed(
            theme="success",
            user_name=ctx.author.name,
            title=CONST.STRINGS["xp_level"].format(xp_data.level),
            footer_text=CONST.STRINGS["xp_server_rank"].format(rank or "NaN"),
            thumbnail_url=ctx.author.display_avatar.url,
            hide_name_in_description=True,
        )
        embed.add_field(
            name=CONST.STRINGS["xp_progress"],
            value=XpService.generate_progress_bar(xp_data.xp, needed_xp_for_next_level),
            inline=False,
        )

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Level(bot))
