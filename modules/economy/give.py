import discord
from discord.ext import commands

from services.currency_service import Currency
from lib.constants import CONST
from lib.embed_builder import EmbedBuilder
from lib.exceptions.LumiExceptions import LumiException


async def cmd(ctx: commands.Context, user: discord.User, amount: int) -> None:
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

    target_currency.add_balance(amount)
    ctx_currency.take_balance(amount)

    ctx_currency.push()
    target_currency.push()

    embed = EmbedBuilder.create_success_embed(
        ctx,
        description=CONST.STRINGS["give_success"].format(
            ctx.author.name,
            Currency.format(amount),
            user.name,
        ),
    )

    await ctx.respond(embed=embed)
