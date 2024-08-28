from discord.ext import commands
from discord import Embed
from lib.const import CONST
from ui.embeds import builder
from datetime import datetime


class Uptime(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.start_time: datetime = datetime.now()

    @commands.hybrid_command(
        name="uptime",
        usage="uptime",
    )
    async def uptime(self, ctx: commands.Context[commands.Bot]) -> None:
        unix_timestamp: int = int(self.start_time.timestamp())

        embed: Embed = builder.create_success_embed(
            ctx,
            author_text=CONST.STRINGS["ping_author"],
            description=CONST.STRINGS["ping_uptime"].format(unix_timestamp),
            footer_text=CONST.STRINGS["ping_footer"].format(
                int(self.bot.latency * 1000),
            ),
        )
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Uptime(bot))
