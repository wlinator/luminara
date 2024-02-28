import json
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from data.Item import Item
from data.ShopItem import ShopItem
from sb_tools import universal

load_dotenv('.env')

active_blackjack_games = {}
special_balance_name = os.getenv("SPECIAL_BALANCE_NAME")
cash_balance_name = os.getenv("CASH_BALANCE_NAME")

with open("config/economy.json") as file:
    json_data = json.load(file)


class AdminCog(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot

    admin = discord.SlashCommandGroup(name="admin", description="Commands only Bot Admins can do.")
    shop = admin.create_subgroup(name="shop", description="Shop managament")

    @shop.command(
        name="insert",
        description="Insert a new item into the shop"
    )
    @commands.check(universal.owner_check)
    async def admin_shop_insert(self, ctx, *,
                                item: discord.Option(choices=Item.get_all_item_names()),
                                price: discord.Option(int),
                                price_special: discord.Option(int),
                                worth: discord.Option(int),
                                description: discord.Option(str, max_length=60)):
        item = Item.get_item_by_display_name(item)
        shop_item = ShopItem(item)

        shop_item.set_price(abs(price))
        shop_item.set_price_special(abs(price_special))
        shop_item.set_worth(abs(worth))
        shop_item.set_description(description)

        price = price if price != 0 else "N/A"
        price_special = price_special if price_special != 0 else "N/A"
        worth = worth if worth != 0 else "N/A"

        embed = discord.Embed(
            color=discord.Color.green(),
            description=f"Added **{item.name}** to the shop for **${price}** or "
                        f"**{price_special} {special_balance_name}** "
                        f"It can be sold by users for **${worth}**"
        )
        embed.add_field(name="description", value=description)

        await ctx.respond(embed=embed)


def setup(sbbot):
    sbbot.add_cog(AdminCog(sbbot))
