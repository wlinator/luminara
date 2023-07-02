import discord

from data.Inventory import Inventory
from data.Item import Item


class ItemHandler:
    def __init__(self, ctx):
        self.ctx = ctx

    async def rave_coin(self, is_won, bet):
        if is_won and bet >= 9000:
            inv = Inventory(self.ctx.author.id)
            item = Item.get_item_by_name("rave_coin")
            inv.add_item(item)
            del inv

            embed = discord.Embed(
                color=discord.Color.embed_background(),
                title="IT'S OVER 9000!!!",
                description=f"Congrats for winning a bet of $9,000 or more! "
                            f"You've been awarded 1 **{item.display_name}**."
            )

            return await self.ctx.respond(embed=embed)

    async def bitch_coin(self, status):
        if status == "player_blackjack":
            inv = Inventory(self.ctx.author.id)
            item = Item.get_item_by_name("bitch_coin")
            inv.add_item(item)
            del inv

            embed = discord.Embed(
                color=discord.Color.embed_background(),
                title="You hit a BlackJack!",
                description=f"Yous a bitch for winning with a natural hand so I gave you 1 "
                            f"**{item.display_name}**."
            )
            embed.set_footer(text="Take a look in /inventory")

            return await self.ctx.respond(embed=embed)
