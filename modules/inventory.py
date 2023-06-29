import json
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from data.Inventory import Inventory
from sb_tools import universal

load_dotenv('.env')

active_blackjack_games = {}
special_balance_name = os.getenv("SPECIAL_BALANCE_NAME")
cash_balance_name = os.getenv("CASH_BALANCE_NAME")

with open("config/economy.json") as file:
    json_data = json.load(file)


class InventoryCog(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot

    @commands.slash_command(
        name="inventory",
        description="Display your inventory.",
        guild_only=True
    )
    @commands.check(universal.channel_check)
    async def inventory(self, ctx):
        inventory = Inventory(ctx.author.id)
        inventory_dict = inventory.get_inventory()

        description = "You don't have any items!" if inventory_dict == {} else None

        embed = discord.Embed(
            color=discord.Color.embed_background(),
            description=description
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)

        for item, quantity in inventory_dict.items():
            if item.name.endswith("_badge"):

                if not embed.description:
                    embed.description = "**Badges:** "

                emote = self.bot.get_emoji(item.emote_id)
                embed.description += f"{emote} "

            else:
                emote = self.bot.get_emoji(item.emote_id)
                embed.add_field(name=f"{emote} {item.display_name.capitalize()}",
                                value=f"*— Amount: `{quantity}`*",
                                inline=False)
        embed.set_footer(text="for more info do /item")

        await ctx.respond(embed=embed)


def setup(sbbot):
    sbbot.add_cog(InventoryCog(sbbot))
