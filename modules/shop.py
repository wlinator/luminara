import json
import locale
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from data.ShopItem import ShopItem
from sb_tools import universal

load_dotenv('.env')
special_balance_name = os.getenv("SPECIAL_BALANCE_NAME")
cash_balance_name = os.getenv("CASH_BALANCE_NAME")

with open("config/economy.json") as file:
    json_data = json.load(file)


class ShopCog(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot

    @commands.slash_command(
        name="shop",
        description="Display the shop.",
        guild_only=True
    )
    @commands.check(universal.beta_check)
    async def shop(self, ctx):
        shop = ShopItem.get_shop_all()

        embed = discord.Embed(
            color=discord.Color.embed_background(),
            title="Racu Shop",
            description="The shop is updated regularly!"
        )
        embed.set_footer(text="do /buy <item>")

        for item in shop:
            emoji = self.bot.get_emoji(item.item.emote_id)
            locale.setlocale(locale.LC_ALL, '')

            if item.price != 0 and item.price_special != 0:
                item.price = locale.format_string("%d", item.price, grouping=True)
                price = f"${item.price} *or* {item.price_special} {special_balance_name}"
            elif item.price == 0:
                price = f"{item.price_special} {special_balance_name}"
            else:
                item.price = locale.format_string("%d", item.price, grouping=True)
                price = f"${item.price}"

            embed.add_field(name=f"{emoji} {item.item.display_name} - {price}",
                            value=f"\n*{item.description}*",
                            inline=False)

        await ctx.respond(embed=embed)


def setup(sbbot):
    sbbot.add_cog(ShopCog(sbbot))
