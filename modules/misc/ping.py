from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="ping",
        usage="ping",
    )
    async def ping(self, ctx: commands.Context[commands.Bot]) -> None:
        await ctx.send(f"Pong! Latency: {self.bot.latency * 1000:.2f}ms")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ping(bot))
