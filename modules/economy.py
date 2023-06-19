import json
import os
import time

import discord
from discord.ext import commands
from dotenv import load_dotenv

from data.Currency import Currency
from data.Dailies import Dailies
from sb_tools import economy_embeds, universal, interaction

load_dotenv('.env')

active_blackjack_games = {}
special_balance_name = os.getenv("SPECIAL_BALANCE_NAME")
cash_balance_name = os.getenv("CASH_BALANCE_NAME")

with open("json/economy.json") as file:
    json_data = json.load(file)


class Economy(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot

    @commands.slash_command(
        name="balance",
        description="See how much cash you have.",
        guild_only=True
    )
    @commands.check(universal.channel_check)
    async def balance(self, ctx):
        cash_balance = Currency.get_cash_balance(ctx.author.id)
        special_balance = Currency.get_special_balance(ctx.author.id)

        await ctx.respond(embed=economy_embeds.currency_balance(ctx, cash_balance, special_balance))

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

        try:
            if currency == "cash":
                author_cash_balance = Currency.get_cash_balance(ctx.author.id)

                if author_cash_balance < amount or author_cash_balance <= 0:
                    return await ctx.respond(embed=economy_embeds.not_enough_cash())

                target_cash_balance = Currency.get_cash_balance(user.id)

                target_new_cash_balance = target_cash_balance + amount
                author_new_cash_balance = author_cash_balance - amount

                Currency.update_cash_balance(user.id, target_new_cash_balance)
                Currency.update_cash_balance(ctx.author.id, author_new_cash_balance)

            elif currency == special_balance_name:
                author_special_balance = Currency.get_special_balance(ctx.author.id)

                if author_special_balance < amount or author_special_balance <= 0:
                    return await ctx.respond(embed=economy_embeds.not_enough_special_balance())

                target_special_balance = Currency.get_special_balance(user.id)

                target_new_special_balance = target_special_balance + amount
                author_new_special_balance = author_special_balance - amount

                Currency.update_special_balance(user.id, target_new_special_balance)
                Currency.update_special_balance(ctx.author.id, author_new_special_balance)

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
        author_special_balance = Currency.get_special_balance(ctx.author.id)

        if author_special_balance < amount or author_special_balance <= 0:
            return await ctx.respond(embed=economy_embeds.not_enough_special_balance())

        view = interaction.ExchangeConfirmation(ctx)
        await ctx.respond(embed=economy_embeds.exchange_confirmation(amount), view=view)
        await view.wait()

        if view.clickedConfirm:
            author_new_special_balance = author_special_balance - amount
            author_new_cash_balance = Currency.get_cash_balance(ctx.author.id) + (amount * 1000)

            Currency.update_cash_balance(ctx.author.id, author_new_cash_balance)
            Currency.update_special_balance(ctx.author.id, author_new_special_balance)

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

        try:
            if currency == "cash_balance":
                current_cash_balance = Currency.get_cash_balance(user.id)
                new_cash_balance = int(current_cash_balance) + amount
                Currency.update_cash_balance(user.id, new_cash_balance)

            else:
                current_special_balance = Currency.get_special_balance(user.id)
                new_special_balance = int(current_special_balance) + amount
                Currency.update_special_balance(user.id, new_special_balance)

        except Exception as e:
            await ctx.channel.respond("Something went wrong. Check console.", ephemeral=True)
            print(e)
            return

        await ctx.respond(embed=economy_embeds.award(user, currency, amount))

    @commands.slash_command(
        name="daily",
        description="Claim your daily cash!",
        guild_only=True
    )
    @commands.check(universal.channel_check)
    async def daily(self, ctx):
        (can_claim, next_claim) = Dailies.cooldown_check(ctx.author.id)
        amount = json_data["daily_reward"]
        current_time = time.time()

        if can_claim:
            await ctx.respond(embed=economy_embeds.daily_claim(amount))

            # give money
            current_cash_balance = Currency.get_cash_balance(ctx.author.id)
            Currency.update_cash_balance(ctx.author.id, current_cash_balance + amount)

            # push daily to DB
            daily = Dailies(
                user_id=ctx.author.id,
                claimed_at=current_time,
                next_available=current_time + json_data["daily_cooldown"]
            )
            daily.push()

        else:
            cooldown = next_claim - current_time

            hours = int(cooldown // 3600)
            minutes = int((cooldown % 3600) // 60)
            seconds = int(cooldown % 60)

            cooldown_text = f"{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"

            await ctx.respond(embed=economy_embeds.daily_wait(cooldown_text))


def setup(sbbot):
    sbbot.add_cog(Economy(sbbot))
