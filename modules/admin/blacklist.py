import discord
from discord.ext import commands

from lib.const import CONST
from services.blacklist_service import BlacklistUserService
from ui.embeds import Builder


class Blacklist(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="blacklist")
    @commands.is_owner()
    async def blacklist_command(
        self,
        ctx: commands.Context[commands.Bot],
        user: discord.User,
        *,
        reason: str | None = None,
    ) -> None:
        """
        Blacklist a user from the bot.

        Parameters
        ----------
        ctx : commands.Context[commands.Bot]
            The context of the command.
        user : discord.User
            The user to blacklist.
        reason : str | None, optional
        """
        blacklist_service = BlacklistUserService(user.id)
        blacklist_service.add_to_blacklist(reason)

        embed = Builder.create_embed(
            theme="success",
            user_name=ctx.author.name,
            author_text=CONST.STRINGS["admin_blacklist_author"],
            description=CONST.STRINGS["admin_blacklist_description"].format(user.name),
            footer_text=CONST.STRINGS["admin_blacklist_footer"],
            hide_time=True,
        )

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Blacklist(bot))
