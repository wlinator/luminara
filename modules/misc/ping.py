from discord.ext import commands

from lib.const import CONST
from ui.embeds import Builder


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="ping")
    async def ping(self, ctx: commands.Context[commands.Bot]) -> None:
        """
        Ping command.

        Parameters
        ----------
        ctx : commands.Context[commands.Bot]
            The context of the command.
        """
        embed = Builder.create_embed(
            theme="success",
            user_name=ctx.author.name,
            author_text=CONST.STRINGS["ping_author"],
            description=CONST.STRINGS["ping_pong"],
            footer_text=CONST.STRINGS["ping_footer"].format(
                round(1000 * self.bot.latency),
            ),
        )

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ping(bot))
