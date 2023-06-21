import json
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from data.BlackJackStats import BlackJackStats
from main import strings
from sb_tools import universal

load_dotenv('.env')

active_blackjack_games = {}
special_balance_name = os.getenv("SPECIAL_BALANCE_NAME")
cash_balance_name = os.getenv("CASH_BALANCE_NAME")

with open("config/economy.json") as file:
    json_data = json.load(file)


class Stats(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot

    stats = discord.SlashCommandGroup("stats", "Racu stats.")

    @stats.command(
        name="all",
        description="Show the stats for all Racu users."
    )
    # @commands.check(universal.channel_check)
    @commands.check(universal.beta_check)
    async def all(self, ctx):
        # collect data
        bj_games_amount = BlackJackStats.count_games()
        (bj_winning_games_amount, bj_losing_games_amount) = BlackJackStats.get_winning_and_losing_amount()
        (bj_total_investment, bj_total_payout) = BlackJackStats.get_investment_and_payout()

        # calculate data
        roi = ((bj_total_payout - bj_total_investment) / bj_total_investment) * 100
        roi = round(roi, 3)

        # output
        embed = discord.Embed(
            title=strings["stats_all_title"]
        )
        embed.add_field(name=strings["stats_all_blackjack"],
                        value=strings["stats_all_gambling_value3"].format(
                            bj_games_amount,
                            bj_winning_games_amount,
                            bj_losing_games_amount,
                            round(bj_total_investment),
                            round(bj_total_payout),
                            roi
                        ))

        await ctx.respond(embed=embed)

    @stats.command(
        name="me",
        description="Show your personal Racu stats."
    )
    # @commands.check(universal.channel_check)
    @commands.check(universal.beta_check)
    async def me(self, ctx):
        pass


def setup(sbbot):
    sbbot.add_cog(Stats(sbbot))
