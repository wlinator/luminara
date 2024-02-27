import json
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from data.Currency import Currency
from sb_tools import economy_embeds, universal

load_dotenv('.env')

special_balance_name = os.getenv("SPECIAL_BALANCE_NAME")
cash_balance_name = os.getenv("CASH_BALANCE_NAME")

with open("config/economy.json") as file:
    json_data = json.load(file)


class AwardCog(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot

    @commands.slash_command(
        name="give",
        description="Give another user some currency.",
        guild_only=True
    )
    @commands.check(universal.channel_check)
    async def give(self, ctx, *,
                   user: discord.Option(discord.Member),
                   currency: discord.Option(choices=["cash", special_balance_name]),
                   amount: discord.Option(int)):

        if ctx.author.id == user.id:
            return await ctx.respond(embed=economy_embeds.give_yourself_error(currency))
        elif user.bot:
            return await ctx.respond(embed=economy_embeds.give_bot_error(currency))

        # Currency handler
        ctx_currency = Currency(ctx.author.id)
        target_currency = Currency(user.id)

        try:
            if currency == "cash":
                author_cash_balance = ctx_currency.cash

                if author_cash_balance < amount or author_cash_balance <= 0:
                    return await ctx.respond(embed=economy_embeds.not_enough_cash())

                target_currency.add_cash(amount)
                ctx_currency.take_cash(amount)

            elif currency == special_balance_name:
                author_special_balance = ctx_currency.special

                if author_special_balance < amount or author_special_balance <= 0:
                    return await ctx.respond(embed=economy_embeds.not_enough_special_balance())

                target_currency.add_special(amount)
                ctx_currency.take_special(amount)

            ctx_currency.push()
            target_currency.push()

        except Exception as e:
            await ctx.channel.respond("Something funky happened.. Tell Tess.", ephemeral=True)
            print(e)
            return

        await ctx.respond(embed=economy_embeds.give(ctx, user, currency, Currency.format(amount)))

    @commands.slash_command(
        name="award",
        description="Award currency - owner only command.",
        guild_only=True
    )
    @commands.check(universal.channel_check)
    @commands.check(universal.owner_check)
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

        await ctx.respond(embed=economy_embeds.award(user, currency, Currency.format(amount)))


def setup(sbbot):
    sbbot.add_cog(AwardCog(sbbot))
