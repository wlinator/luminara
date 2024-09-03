import discord
from discord.ext import commands

import lib.format
from lib.client import Luminara
from lib.const import CONST
from services.currency_service import Currency
from ui.embeds import Builder


class Award(commands.Cog):
    def __init__(self, bot: Luminara):
        self.bot = bot
        self.award_command.usage = lib.format.generate_usage(self.award_command)

    @commands.command(name="award", aliases=["aw"])
    @commands.is_owner()
    async def award_command(
        self,
        ctx: commands.Context[Luminara],
        user: discord.User,
        amount: int,
    ) -> None:
        """
        Award a user with a specified amount of currency.

        Parameters
        ----------
        ctx : commands.Context[Luminara]
            The context of the command.
        user : discord.User
            The user to award.
        amount : int
            The amount of currency to award.
        """
        curr = Currency(user.id)
        curr.add_balance(amount)
        curr.push()

        embed = Builder.create_embed(
            Builder.SUCCESS,
            user_name=ctx.author.name,
            author_text=CONST.STRINGS["admin_award_title"],
            description=CONST.STRINGS["admin_award_description"].format(
                Currency.format(amount),
                user.name,
            ),
        )

        await ctx.send(embed=embed)


async def setup(bot: Luminara) -> None:
    await bot.add_cog(Award(bot))
