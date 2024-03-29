import discord

from services.Currency import Currency


async def cmd(ctx):
    # Currency handler
    ctx_currency = Currency(ctx.author.id)

    balance = Currency.format(ctx_currency.balance)

    embed = discord.Embed(
        color=discord.Color.embed_background(),
        description=f"**Cash**: ${balance}"
    )
    embed.set_author(name=f"{ctx.author.name}'s wallet", icon_url=ctx.author.avatar.url)

    await ctx.respond(embed=embed)
