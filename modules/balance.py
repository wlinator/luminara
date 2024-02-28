import json
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from services.Currency import Currency
from utils import checks

load_dotenv('.env')

special_balance_name = os.getenv("SPECIAL_BALANCE_NAME")
cash_balance_name = os.getenv("CASH_BALANCE_NAME")


class BalanceCog(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.slash_command(
        name="balance",
        description="See how much cash you have.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def balance(self, ctx):
        # Currency handler
        ctx_currency = Currency(ctx.author.id)

        cash_balance = Currency.format(ctx_currency.cash)
        special_balance = Currency.format(ctx_currency.special)

        embed = discord.Embed(
            color=discord.Color.embed_background(),
            description=f"**Cash**: {cash_balance_name}{cash_balance}\n"
                        f"**{special_balance_name.capitalize()}**: {special_balance}"
        )
        embed.set_author(name=f"{ctx.author.name}'s wallet", icon_url=ctx.author.avatar.url)
        embed.set_footer(text=f"Level up to earn {special_balance_name}!")

        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(BalanceCog(client))
