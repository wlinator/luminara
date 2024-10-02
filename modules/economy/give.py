import discord
from discord.ext import commands

import lib.format
from lib.client import Luminara
from lib.const import CONST
from lib.exceptions import LumiException
from services.currency_service import Currency
from ui.embeds import Builder


class Give(commands.Cog):
    def __init__(self, bot: Luminara) -> None:
        self.bot: Luminara = bot
        self.give.usage = lib.format.generate_usage(self.give)

    @commands.hybrid_command(
        name="give",
    )
    @commands.guild_only()
    async def give(
        self,
        ctx: commands.Context[Luminara],
        user: discord.User,
        amount: int,
    ) -> None:
        """
        Give currency to another user.

        Parameters
        ----------
        ctx : commands.Context[Luminara]
            The context of the command.
        user : discord.User
            The user to give currency to.
        amount : int
            The amount of currency to give.
        """
        if ctx.author.id == user.id:
            raise LumiException(CONST.STRINGS["give_error_self"])
        if user.bot:
            raise LumiException(CONST.STRINGS["give_error_bot"])
        if amount <= 0:
            raise LumiException(CONST.STRINGS["give_error_invalid_amount"])

        ctx_currency = Currency(ctx.author.id)
        target_currency = Currency(user.id)

        if ctx_currency.balance < amount:
            raise LumiException(CONST.STRINGS["give_error_insufficient_funds"])

        ctx_currency.take_balance(amount)
        target_currency.add_balance(amount)

        ctx_currency.push()
        target_currency.push()

        embed = Builder.create_embed(
            Builder.SUCCESS,
            user_name=ctx.author.name,
            description=CONST.STRINGS["give_success"].format(Currency.format(amount), user.name),
        )

        await ctx.send(embed=embed)


async def setup(bot: Luminara) -> None:
    await bot.add_cog(Give(bot))
