from discord.ext import commands

import lib.format
from lib.const import CONST
from ui.embeds import Builder
from ui.views.invite import InviteButton


class Invite(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.invite.usage = lib.format.generate_usage(self.invite)

    @commands.hybrid_command(name="invite", aliases=["inv"])
    async def invite(self, ctx: commands.Context[commands.Bot]) -> None:
        """
        Invite command.

        Parameters
        ----------
        ctx : commands.Context[commands.Bot]
            The context of the command.
        """
        await ctx.send(
            embed=Builder.create_embed(
                theme="success",
                user_name=ctx.author.name,
                author_text=CONST.STRINGS["invite_author"],
                description=CONST.STRINGS["invite_description"],
            ),
            view=InviteButton(),
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Invite(bot))
