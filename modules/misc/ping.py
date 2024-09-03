from discord.ext import commands

import lib.format
from lib.client import Luminara
from lib.const import CONST
from ui.embeds import Builder


class Ping(commands.Cog):
    def __init__(self, bot: Luminara):
        self.bot = bot
        self.ping.usage = lib.format.generate_usage(self.ping)

    @commands.hybrid_command(name="ping")
    async def ping(self, ctx: commands.Context[Luminara]) -> None:
        """
        Show Luminara's latency.

        Parameters
        ----------
        ctx : commands.Context[Luminara]
            The context of the command.
        """
        embed = Builder.create_embed(
            Builder.SUCCESS,
            user_name=ctx.author.name,
            author_text=CONST.STRINGS["ping_author"],
            description=CONST.STRINGS["ping_pong"],
            footer_text=CONST.STRINGS["ping_footer"].format(
                round(1000 * self.bot.latency),
            ),
        )

        await ctx.send(embed=embed)


async def setup(bot: Luminara) -> None:
    await bot.add_cog(Ping(bot))
