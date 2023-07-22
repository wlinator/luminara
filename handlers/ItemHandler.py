import logging

from data.Inventory import Inventory
from data.Item import Item

racu_logs = logging.getLogger('Racu.Core')


class ItemHandler:
    def __init__(self, ctx):
        self.ctx = ctx

    async def rave_coin(self, is_won, bet, field):
        if is_won and bet >= 9000:
            inv = Inventory(self.ctx.author.id)
            item = Item.get_item_by_name("rave_coin")
            inv.add_item(item)

            field += f"- **1 {item.display_name}**.\n"
            racu_logs.info(f"{self.ctx.author.name} was given 1 rave_coin (ItemHandler: bet > 9000)")

            return field

        return field

    async def bitch_coin(self, status, field):
        if status == "player_blackjack":
            inv = Inventory(self.ctx.author.id)
            item = Item.get_item_by_name("bitch_coin")
            inv.add_item(item)

            field += f"- **1 {item.display_name}**.\n"

            racu_logs.info(f"{self.ctx.author.name} was given 1 bitch_coin (ItemHandler: player_blackjack)")
            return field

        return field
