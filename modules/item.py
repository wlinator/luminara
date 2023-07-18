import json
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from data.Currency import Currency
from data.Inventory import Inventory
from data.Item import Item
from data.ShopItem import ShopItem
from sb_tools import universal

load_dotenv('.env')

active_blackjack_games = {}
special_balance_name = os.getenv("SPECIAL_BALANCE_NAME")
cash_balance_name = os.getenv("CASH_BALANCE_NAME")

with open("config/economy.json") as file:
    json_data = json.load(file)


class ItemCog(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot

    @commands.slash_command(
        name="item",
        description="View the information about a specific item.",
        guild_only=True
    )
    @commands.check(universal.channel_check)
    async def item_command(self, ctx, *, item: discord.Option(choices=Item.get_all_item_names())):
        # create item object from choice
        item = Item.get_item_by_display_name(item)
        amount = item.get_quantity(ctx.author.id)

        shop_item = ShopItem(item)
        price = "can't be bought" if shop_item.price <= 0 else f"${Currency.format(shop_item.price)}"
        worth = "can't be sold" if shop_item.worth <= 0 else f"${Currency.format(shop_item.worth)}"

        if shop_item.price_special > 0:
            if price == "can't be bought":
                price = f"{shop_item.price_special} {special_balance_name}"
            else:
                price += f" or {shop_item.price_special} {special_balance_name}"

        emote = self.bot.get_emoji(item.emote_id)

        amount_string = f"You have this item {amount} time"

        if amount > 1:
            amount_string += "s"
        elif amount < 1:
            amount_string = f"You don't have this item"

        if item.quote is None or item.quote == "":
            description = amount_string
        else:
            description = f"> *{item.quote}*\n\n{amount_string}"

        embed = discord.Embed(
            color=discord.Color.embed_background(),
            title=f"{emote} {item.display_name.capitalize()}",
            description=description
        )

        embed.add_field(name="Value", value=f"`/shop` price: **{price}**\n`/sell` value: **{worth}**", inline=False)

        embed.add_field(name="Description", value=item.description, inline=False)
        embed.set_thumbnail(url=item.image_url)
        embed.set_footer(text=f"type: {item.type}")

        return await ctx.respond(embed=embed)

    items = discord.SlashCommandGroup(name="items")

    @items.command(
        name="gift",
        description="Award items to someone."
    )
    @commands.check(universal.owner_check)
    async def gift(self, ctx, *,
                   user: discord.Option(discord.Member),
                   item: discord.Option(choices=Item.get_all_item_names()),
                   quantity: discord.Option(int)):

        try:
            item = Item.get_item_by_display_name(item)
            target_inventory = Inventory(user.id)
            target_inventory.add_item(item, quantity)

        except Exception as e:
            await ctx.channel.respond("Something went wrong. Check console.", ephemeral=True)
            print(e)
            return

        embed = discord.Embed(
            color=discord.Color.embed_background(),
            description=f"Awarded **{abs(quantity)} {item.name}** to {user.name}."
        )

        await ctx.respond(embed=embed)


def setup(sbbot):
    sbbot.add_cog(ItemCog(sbbot))
