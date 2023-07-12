import json
import locale
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from data.Currency import Currency
from sb_tools import economy_embeds, universal, interaction

load_dotenv('.env')

active_blackjack_games = {}
special_balance_name = os.getenv("SPECIAL_BALANCE_NAME")
cash_balance_name = os.getenv("CASH_BALANCE_NAME")

with open("config/economy.json") as file:
    json_data = json.load(file)


class EconomyCog(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot

    @commands.slash_command(
        name="balance",
        description="See how much cash you have.",
        guild_only=True
    )
    @commands.check(universal.channel_check)
    async def balance(self, ctx):

        # Currency handler
        ctx_currency = Currency(ctx.author.id)

        locale.setlocale(locale.LC_ALL, '')
        cash_balance = locale.format_string("%d", ctx_currency.cash, grouping=True)
        special_balance = locale.format_string("%d", ctx_currency.special, grouping=True)

        embed = discord.Embed(
            color=discord.Color.embed_background(),
            description=f"**Cash**: {cash_balance_name}{cash_balance}\n"
                        f"**{special_balance_name.capitalize()}**: {special_balance}"
        )
        embed.set_author(name=f"{ctx.author.name}'s wallet", icon_url=ctx.author.avatar.url)
        embed.set_footer(text=f"Level up to earn {special_balance_name}!")

        await ctx.respond(embed=embed)

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

        await ctx.respond(embed=economy_embeds.give(ctx, user, currency, amount))

    @commands.slash_command(
        name="exchange",
        description=f"Exchange {special_balance_name} for cash.",
        guild_only=True
    )
    @commands.check(universal.channel_check)
    async def exchange(self, ctx, *, amount: discord.Option(int)):

        # Currency handler
        ctx_currency = Currency(ctx.author.id)

        author_special_balance = ctx_currency.special

        if author_special_balance < amount or author_special_balance <= 0:
            return await ctx.respond(embed=economy_embeds.not_enough_special_balance())

        view = interaction.ExchangeConfirmation(ctx)
        await ctx.respond(embed=economy_embeds.exchange_confirmation(amount), view=view)
        await view.wait()

        if view.clickedConfirm:
            exchange_rate = 1000

            ctx_currency.add_cash(amount * exchange_rate)
            ctx_currency.take_special(amount)
            ctx_currency.push()

            return await ctx.edit(embed=economy_embeds.exchange_done(amount))

        await ctx.edit(embed=economy_embeds.exchange_stopped())

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

        await ctx.respond(embed=economy_embeds.award(user, currency, amount))


def setup(sbbot):
    sbbot.add_cog(EconomyCog(sbbot))
