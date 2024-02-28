import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from services.Currency import Currency
from main import economy_config
from lib import economy_embeds, checks, interaction

load_dotenv('.env')

special_balance_name = os.getenv("SPECIAL_BALANCE_NAME")
cash_balance_name = os.getenv("CASH_BALANCE_NAME")


class ExchangeCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        name="exchange",
        description=f"Exchange {special_balance_name} for cash.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def exchange(self, ctx, *, amount: discord.Option(int)):

        # Currency handler
        ctx_currency = Currency(ctx.author.id)
        author_special_balance = ctx_currency.special
        exchange_rate = economy_config["exchange_rate"]
        total = amount * exchange_rate

        if author_special_balance < amount or author_special_balance <= 0:
            return await ctx.respond(embed=economy_embeds.not_enough_special_balance())

        view = interaction.ExchangeConfirmation(ctx)
        embed = discord.Embed(
            description=f"You're about to sell **{amount} {special_balance_name}** for **{cash_balance_name}{Currency.format(total)}**. "
                        f"Are you absolutely sure about this?"
        )
        await ctx.respond(embed=embed, view=view)
        await view.wait()

        if view.clickedConfirm:
            ctx_currency.add_cash(total)
            ctx_currency.take_special(amount)
            ctx_currency.push()

            embed.colour = discord.Color.green()
            embed.description = f"You successfully exchanged **{amount} {special_balance_name}** " \
                                f"for **{cash_balance_name}{Currency.format(total)}**."

            return await ctx.edit(embed=embed)

        embed.colour = discord.Color.red()
        embed.description = "The exchange was canceled."
        await ctx.edit(embed=embed)


def setup(client):
    client.add_cog(ExchangeCog(client))
