import json
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from services.BlackJackStats import BlackJackStats
from services.Currency import Currency
from services.SlotsStats import SlotsStats
from main import strings, economy_config
from lib import checks

load_dotenv('.env')

active_blackjack_games = {}
special_balance_name = os.getenv("SPECIAL_BALANCE_NAME")
cash_balance_name = os.getenv("CASH_BALANCE_NAME")

with open("config/economy.json") as file:
    json_data = json.load(file)


class StatsCog(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.slash_command(
        name="stats",
        description="Display your stats (BETA)",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def stats(self, ctx, *, game: discord.Option(choices=["BlackJack", "Slots"])):
        output = ""

        if game == "BlackJack":
            stats = BlackJackStats.get_user_stats(ctx.author.id)

            # amount formatting
            total_bet = Currency.format_human(stats["total_bet"])
            total_payout = Currency.format_human(stats["total_payout"])

            # output = f"{ctx.author.name}'s racu stats\n\n"
            output = strings["stats_blackjack"].format(
                stats["amount_of_games"],
                total_bet,
                stats["winning_amount"],
                total_payout
            )

        elif game == "Slots":
            stats = SlotsStats.get_user_stats(ctx.author.id)

            # amount formatting
            total_bet = Currency.format_human(stats["total_bet"])
            total_payout = Currency.format_human(stats["total_payout"])

            output = strings["stats_slots"].format(stats["amount_of_games"], total_bet, total_payout)
            output += "\n\n"

            pair_emote = self.bot.get_emoji(economy_config["slots"]["emotes"]["slots_0_id"])
            three_emote = self.bot.get_emoji(economy_config["slots"]["emotes"]["slots_4_id"])
            diamonds_emote = self.bot.get_emoji(economy_config["slots"]["emotes"]["slots_5_id"])
            seven_emote = self.bot.get_emoji(economy_config["slots"]["emotes"]["slots_6_id"])

            output += f"{pair_emote} | **{stats['games_won_pair']}** pairs.\n"
            output += f"{three_emote} | **{stats['games_won_three_of_a_kind']}** three-of-a-kinds.\n"
            output += f"{diamonds_emote} | **{stats['games_won_three_diamonds']}** triple diamonds.\n"
            output += f"{seven_emote} | **{stats['games_won_jackpot']}** jackpots."

        output += "\n\n *This command is still in beta, stats may be slightly inaccurate.*"
        await ctx.respond(content=output)


def setup(client):
    client.add_cog(StatsCog(client))
