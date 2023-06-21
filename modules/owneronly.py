import json
import os
import sqlite3

import discord
from discord.ext import commands
from dotenv import load_dotenv

from db import database
from sb_tools import universal

load_dotenv('.env')

active_blackjack_games = {}
special_balance_name = os.getenv("SPECIAL_BALANCE_NAME")
cash_balance_name = os.getenv("CASH_BALANCE_NAME")

with open("config/economy.json") as file:
    json_data = json.load(file)


class OwnerOnly(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot

    sql = discord.SlashCommandGroup(name="sql", description="Perform SQL commands (DANGEROUS)")

    @sql.command(
        name="select",
        description="Perform a SELECT query in the database.",
        guild_only=True
    )
    @commands.check(universal.owner_check)
    async def select(self, ctx, *, query: discord.Option(str)):
        if query.lower().startswith("select "):
            query = query[7:]

        try:
            results = database.select_query(f"SELECT {query}")
        except sqlite3.Error as error:
            results = error

        return await ctx.respond(content=f"```SELECT {query}```\n```{results}```", ephemeral=True)

    @sql.command(
        name="inject",
        description="Change a value in the database. (DANGEROUS)",
        guild_only=True
    )
    @commands.check(universal.owner_check)
    async def inject(self, ctx, *, query: discord.Option(str)):
        try:
            database.execute_query(query)
            await ctx.respond(content=f"That worked!\n```{query}```", ephemeral=True)
        except sqlite3.Error as error:
            await ctx.respond(content=f"Query:\n```{query}```\nError message:\n```{error}```", ephemeral=True)


def setup(sbbot):
    sbbot.add_cog(OwnerOnly(sbbot))
