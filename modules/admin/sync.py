import discord
from discord.ext import commands

from lib.const import CONST
from ui.embeds import Builder


class Sync(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        name="sync",
        usage="sync [guild]",
    )
    @commands.guild_only()
    @commands.is_owner()
    async def sync(
        self,
        ctx: commands.Context[commands.Bot],
        guild: discord.Guild | None = None,
    ) -> None:
        if not guild:
            guild = ctx.guild

        assert guild

        self.bot.tree.copy_global_to(guild=guild)
        await self.bot.tree.sync(guild=guild)

        embed = Builder.create_embed(
            theme="success",
            user_name=ctx.author.name,
            author_text=CONST.STRINGS["sync_author"],
            description=CONST.STRINGS["sync_description"],
        )

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Sync(bot))
