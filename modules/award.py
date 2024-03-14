import json
import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv

from services.Currency import Currency
from lib import checks

load_dotenv('.env')
logs = logging.getLogger('Racu.Core')

with open("config/economy.json") as file:
    json_data = json.load(file)


class AwardCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        name="award",
        description="Award currency - owner only command.",
        guild_only=True
    )
    @commands.check(checks.channel)
    @commands.check(checks.bot_owner)
    async def award(self, ctx, *, user: discord.Option(discord.Member), amount: discord.Option(int)):

        # Currency handler
        curr = Currency(user.id)
        curr.add_balance(amount)
        curr.push()

        embed = discord.Embed(
            color=discord.Color.green(),
            description=f"Awarded **${Currency.format(amount)}** to {user.name}."
        )

        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(AwardCog(client))
