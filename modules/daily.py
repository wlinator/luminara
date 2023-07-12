import json
import os
from datetime import datetime

from discord.ext import commands
from dotenv import load_dotenv

from data.Dailies import Dailies
from main import strings
from sb_tools import universal

load_dotenv('.env')

active_blackjack_games = {}
special_balance_name = os.getenv("SPECIAL_BALANCE_NAME")

with open("config/economy.json") as file:
    json_data = json.load(file)


class DailyCog(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot

    @commands.slash_command(
        name="daily",
        description="Claim your daily cash!",
        guild_only=True
    )
    @commands.check(universal.channel_check)
    async def daily(self, ctx):
        ctx_daily = Dailies(ctx.author.id)

        if not ctx_daily.can_be_claimed():
            return await ctx.respond(content=strings["daily_no_claim"].format(ctx.author.name))

        ctx_daily.streak = ctx_daily.streak + 1 if ctx_daily.streak_check() else 1
        ctx_daily.claimed_at = datetime.now(tz=ctx_daily.tz).isoformat()
        ctx_daily.amount = int(50 * (1.2 * (ctx_daily.streak - 1)))

        ctx_daily.refresh()

        output = strings["daily_claim"].format(ctx.author.name, ctx_daily.amount)

        if ctx_daily.streak > 1:
            output += "\n" + strings["daily_streak"].format(ctx_daily.streak)

        await ctx.respond(content=output)


def setup(sbbot):
    sbbot.add_cog(DailyCog(sbbot))
