import discord
from discord.ext import commands

import lib.format
from lib.const import CONST


class Dev(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.sync.usage = lib.format.generate_usage(self.sync)
        self.clear.usage = lib.format.generate_usage(self.clear)

    @commands.group(name="dev", description="Lumi developer commands")
    @commands.guild_only()
    @commands.is_owner()
    async def dev(self, ctx: commands.Context[commands.Bot]) -> None:
        pass

    @dev.command(
        name="sync_tree",
        aliases=["sync"],
    )
    async def sync(
        self,
        ctx: commands.Context[commands.Bot],
        guild: discord.Guild | None = None,
    ) -> None:
        """
        Sync the bot's tree to the specified guild.

        Parameters
        ----------
        ctx : commands.Context[commands.Bot]
            The context of the command.
        guild : discord.Guild | None, optional
            The guild to sync the tree to, by default None.
        """
        if guild:
            self.bot.tree.copy_global_to(guild=guild)

        await self.bot.tree.sync(guild=guild)

        await ctx.send(content=CONST.STRINGS["dev_sync_tree"])

    @dev.command(
        name="clear_tree",
        aliases=["clear"],
    )
    async def clear(
        self,
        ctx: commands.Context[commands.Bot],
        guild: discord.Guild | None = None,
    ) -> None:
        """
        Clear the bot's tree for the specified guild.

        Parameters
        ----------
        ctx : commands.Context[commands.Bot]
            The context of the command.
        guild : discord.Guild | None, optional
        """
        self.bot.tree.clear_commands(guild=guild)

        await ctx.send(content=CONST.STRINGS["dev_clear_tree"])


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Dev(bot))
