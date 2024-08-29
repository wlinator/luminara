import discord
from discord.ext import commands

from lib.const import CONST


class Dev(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(name="dev", description="Lumi developer commands")
    @commands.guild_only()
    @commands.is_owner()
    async def dev(self, ctx: commands.Context[commands.Bot]) -> None:
        pass

    @dev.command(
        name="sync_tree",
        aliases=["sync"],
        usage="sync_tree [guild]",
    )
    async def sync(
        self,
        ctx: commands.Context[commands.Bot],
        guild: discord.Guild | None = None,
    ) -> None:
        if guild:
            self.bot.tree.copy_global_to(guild=guild)

        await self.bot.tree.sync(guild=guild)

        await ctx.send(content=CONST.STRINGS["dev_sync_tree"])

    @dev.command(name="clear_tree", aliases=["clear"])
    async def sync_global(
        self,
        ctx: commands.Context[commands.Bot],
        guild: discord.Guild | None = None,
    ) -> None:
        self.bot.tree.clear_commands(guild=guild)

        await ctx.send(content=CONST.STRINGS["dev_clear_tree"])


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Dev(bot))
