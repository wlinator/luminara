import logging

from data import Item
from db import database

racu_logs = logging.getLogger('Racu.Core')


class Inventory:
    def __init__(self, user_id):
        self.user_id = user_id

    def add_item(self, item: Item.Item, quantity=1):
        """
        Adds an item with a specific count (default 1) to the database, if there are
        no records of this user having that item yet, it will just add a record with quantity=quantity.
        :param item:
        :param quantity:
        :return:
        """

        query = """
        INSERT OR REPLACE INTO inventory (user_id, item_id, quantity)
        VALUES (?, ?, COALESCE((SELECT quantity FROM inventory WHERE user_id = ? AND item_id = ?), 0) + ?)
        """

        database.execute_query(query, (self.user_id, item.id, self.user_id, item.id, abs(quantity)))

    def get_inventory(self):
        query = "SELECT item_id, quantity FROM inventory WHERE user_id = ? AND quantity > 0"
        results = database.select_query(query, (self.user_id,))

        items_dict = {}
        for row in results:
            item_id, quantity = row
            item = Item.Item(item_id)
            items_dict[item] = quantity

        return items_dict

    def get_item_quantity(self, item: Item.Item):
        query = "SELECT COALESCE(quantity, 0) FROM inventory WHERE user_id = ? AND item_id = ?"
        result = database.select_query_one(query, (self.user_id, item.id))
        return result

    def get_sell_data(self):
        query = """
                SELECT item.display_name
                FROM inventory
                JOIN ShopItem ON inventory.item_id = ShopItem.item_id
                JOIN item ON inventory.item_id = item.id
                WHERE inventory.user_id = ? AND inventory.quantity > 0 AND ShopItem.worth > 0
                """

        try:
            item_names = []
            results = database.select_query(query, (self.user_id,))

            for item in results:
                item_names.append(item[0])

            return item_names

        except Exception as e:
            racu_logs.error(e)
            return []
