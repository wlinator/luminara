import json
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from services.Currency import Currency
from lib import economy_embeds, checks

load_dotenv('.env')

special_balance_name = os.getenv("SPECIAL_BALANCE_NAME")
cash_balance_name = os.getenv("CASH_BALANCE_NAME")

with open("config/economy.json") as file:
    json_data = json.load(file)


class AwardCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        name="give",
        description="Give another user some currency.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def give(self, ctx, *, user: discord.Option(discord.Member), amount: discord.Option(int)):

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
            author_cash_balance = ctx_currency.cash

            if author_cash_balance < amount or author_cash_balance <= 0:
                return await ctx.respond(embed=economy_embeds.not_enough_cash())

            target_currency.add_cash(amount)
            ctx_currency.take_cash(amount)

            ctx_currency.push()
            target_currency.push()

        except Exception as e:
            await ctx.channel.respond("Something funky happened.. Sorry about that.", ephemeral=True)
            print(e)
            return

        embed = discord.Embed(
            color=discord.Color.green(),
            description=f"**{ctx.author.name}** gave **${Currency.format(amount)}** to {user.name}."
        )
        embed.set_footer(text="Say thanks! :)")

        await ctx.respond(embed=embed)

    @commands.slash_command(
        name="award",
        description="Award currency - owner only command.",
        guild_only=True
    )
    @commands.check(checks.channel)
    @commands.check(checks.bot_owner)
    async def award(self, ctx, *,
                    user: discord.Option(discord.Member),
                    currency: discord.Option(choices=["cash_balance", "special_balance"]),
                    amount: discord.Option(int)):

        # Currency handler
        target_currency = Currency(user.id)

        try:
            if currency == "cash_balance":
                target_currency.add_cash(amount)

            else:
                target_currency.add_special(amount)

            target_currency.push()

        except Exception as e:
            await ctx.channel.respond("Something went wrong. Check console.", ephemeral=True)
            print(e)
            return

        embed = discord.Embed(
            color=discord.Color.green(),
            description=f"Awarded **${Currency.format(amount)}** to {user.name}."
        )

        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(AwardCog(client))
