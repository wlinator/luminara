import json
import os
from datetime import datetime, timedelta

from discord.ext import commands
from dotenv import load_dotenv

import utils.time
from services.Dailies import Dailies
from services.Currency import Currency
from main import strings
from utils import checks

load_dotenv('.env')

active_blackjack_games = {}
special_balance_name = os.getenv("SPECIAL_BALANCE_NAME")

with open("config/economy.json") as file:
    json_data = json.load(file)


class DailyCog(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.slash_command(
        name="daily",
        description="Claim your daily cash!",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def daily(self, ctx):
        ctx_daily = Dailies(ctx.author.id)

        if not ctx_daily.can_be_claimed():
            wait_time = datetime.now() + timedelta(seconds=utils.time.seconds_until(7, 0))
            unix_time = int(round(wait_time.timestamp()))

            return await ctx.respond(content=strings["daily_no_claim"].format(ctx.author.name, unix_time))

        ctx_daily.streak = ctx_daily.streak + 1 if ctx_daily.streak_check() else 1
        ctx_daily.claimed_at = datetime.now(tz=ctx_daily.tz).isoformat()
        ctx_daily.amount = int(100 * (12 * (ctx_daily.streak - 1)))

        ctx_daily.refresh()

        output = strings["daily_claim"].format(ctx.author.name, Currency.format(ctx_daily.amount))

        if ctx_daily.streak > 1:
            output += "\n" + strings["daily_streak"].format(ctx_daily.streak)

        await ctx.respond(content=output)


def setup(client):
    client.add_cog(DailyCog(client))
