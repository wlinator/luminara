import json
import os

import discord
from discord.ext import commands, bridge
from dotenv import load_dotenv

from services.Inventory import Inventory
from lib import checks

load_dotenv('.env')

with open("config/economy.json") as file:
    json_data = json.load(file)


class InventoryCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @bridge.bridge_command(
        name="inventory",
        aliases=["inv"],
        description="Display your inventory.",
        help="Display your inventory, this will also show your Racu badges if you have any.",
        guild_only=True
    )
    @commands.check(checks.channel)
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
            if item.type == "badge":

                if not embed.description:
                    embed.description = "**Badges:** "

                emote = self.client.get_emoji(item.emote_id)
                embed.description += f"{emote} "

            else:
                emote = self.client.get_emoji(item.emote_id)
                embed.add_field(name=f"{emote} {item.display_name.capitalize()}",
                                value=f"*— amount: `{quantity}`*",
                                inline=False)

        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(InventoryCog(client))
