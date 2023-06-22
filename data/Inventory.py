from data import Item
from db import database


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

        database.execute_query(query, (self.user_id, item.item_id, self.user_id, item.item_id, quantity))

    def get_inventory(self):
        query = "SELECT item_id, quantity FROM inventory WHERE user_id = ? AND quantity > 0"
        results = database.select_query(query, (self.user_id,))

        items_dict = {}
        for row in results:
            item_id, quantity = row
            item = Item.Item(item_id)
            items_dict[item] = quantity

        print(items_dict)
        return items_dict

    def get_item_quantity(self, item: Item.Item):
        query = "SELECT quantity FROM inventory WHERE user_id = ? AND item_id = ?"

        result = database.select_query_one(query, (self.user_id, item.item_id))

        if result:
            return result[0]

        return 0
