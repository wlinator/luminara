from discord.ext import commands
from lib.const import CONST
from ui.embeds import builder


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="ping",
        usage="ping",
    )
    async def ping(self, ctx: commands.Context[commands.Bot]) -> None:
        embed = builder.create_success_embed(
            ctx,
            author_text=CONST.STRINGS["ping_author"],
            description=CONST.STRINGS["ping_pong"],
            footer_text=CONST.STRINGS["ping_footer"].format(
                round(1000 * self.bot.latency),
            ),
        )

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ping(bot))
