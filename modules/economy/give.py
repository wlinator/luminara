import discord

from lib.embeds.error import EconErrors
from services.Currency import Currency


async def cmd(ctx, user, amount):
    if ctx.author.id == user.id:
        embed = discord.Embed(
            color=discord.Color.red(),
            description=f"You can't give money to yourself, silly."
        )
        return await ctx.respond(embed=embed)
    elif user.bot:
        embed = discord.Embed(
            color=discord.Color.red(),
            description=f"You can't give money to a bot, silly."
        )
        return await ctx.respond(embed=embed)

    # Currency handler
    ctx_currency = Currency(ctx.author.id)
    target_currency = Currency(user.id)

    try:
        author_balance = ctx_currency.balance

        if author_balance < amount or author_balance <= 0:
            return await ctx.respond(embed=EconErrors.insufficient_balance(ctx))

        target_currency.add_balance(amount)
        ctx_currency.take_balance(amount)

        ctx_currency.push()
        target_currency.push()

    except Exception as e:
        await ctx.respond("Something funky happened.. Sorry about that.", ephemeral=True)
        print(e)
        return

    embed = discord.Embed(
        color=discord.Color.green(),
        description=f"**{ctx.author.name}** gave **${Currency.format(amount)}** to {user.name}."
    )
    embed.set_footer(text="Say thanks! :)")

    await ctx.respond(embed=embed)
