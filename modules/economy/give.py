import discord
from discord.ext import commands

from services.currency_service import Currency


async def cmd(ctx, user, amount):
    if ctx.author.id == user.id:
        raise commands.BadArgument("you can't give money to yourself.")
    elif user.bot:
        raise commands.BadArgument("you can't give money to a bot.")
    elif amount <= 0:
        raise commands.BadArgument("invalid amount.")

    # Currency handler
    ctx_currency = Currency(ctx.author.id)
    target_currency = Currency(user.id)

    author_balance = ctx_currency.balance

    if author_balance < amount or author_balance <= 0:
        raise commands.BadArgument("you don't have enough cash.")

    target_currency.add_balance(amount)
    ctx_currency.take_balance(amount)

    ctx_currency.push()
    target_currency.push()

    embed = discord.Embed(
        color=discord.Color.green(),
        description=f"**{ctx.author.name}** gave **${Currency.format(amount)}** to {user.name}.",
    )

    await ctx.respond(embed=embed)
