import discord
from discord.ext import commands

import lib.format
from lib.client import Luminara
from lib.const import CONST


class Dev(commands.Cog):
    def __init__(self, bot: Luminara):
        self.bot = bot
        self.sync.usage = lib.format.generate_usage(self.sync)
        self.clear.usage = lib.format.generate_usage(self.clear)
        self.stop.usage = lib.format.generate_usage(self.stop)

    @commands.group(name="dev", description="Lumi developer commands")
    @commands.guild_only()
    @commands.is_owner()
    async def dev(self, ctx: commands.Context[Luminara]) -> None:
        """
        Luminara developer commands
        """

    @dev.command(
        name="sync_tree",
        aliases=["sync"],
    )
    async def sync(
        self,
        ctx: commands.Context[Luminara],
        guild: discord.Guild | None = None,
    ) -> None:
        """
        Sync the bot's tree to the specified guild.

        Parameters
        ----------
        ctx : commands.Context[Luminara]
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
        ctx: commands.Context[Luminara],
        guild: discord.Guild | None = None,
    ) -> None:
        """
        Clear the bot's tree for the specified guild.

        Parameters
        ----------
        ctx : commands.Context[Luminara]
            The context of the command.
        guild : discord.Guild | None, optional
        """
        self.bot.tree.clear_commands(guild=guild)

        await ctx.send(content=CONST.STRINGS["dev_clear_tree"])

    @dev.command(
        name="stop",
        usage="dev stop",
    )
    @commands.is_owner()
    async def stop(
        self,
        ctx: commands.Context[Luminara],
    ) -> None:
        """
        Stops the bot. If Tux is running with Docker Compose, this will restart the container.

        Parameters
        ----------
        ctx : commands.Context
            The context in which the command is being invoked.
        """

        await ctx.reply(CONST.STRINGS["dev_stop_note"])
        await self.bot.shutdown()


async def setup(bot: Luminara) -> None:
    await bot.add_cog(Dev(bot))
