import discord

from services.currency_service import Currency


async def cmd(ctx, user: discord.User, amount: int):
    # Currency handler
    curr = Currency(user.id)
    curr.add_balance(amount)
    curr.push()

    embed = discord.Embed(
        color=discord.Color.green(),
        description=f"Awarded **${Currency.format(amount)}** to {user.name}.",
    )

    await ctx.respond(embed=embed)
