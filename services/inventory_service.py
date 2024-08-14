from loguru import logger

from db import database
from services import item_service


class Inventory:
    def __init__(self, user_id):
        self.user_id = user_id

    def add_item(self, item: item_service.Item, quantity=1):
        """
        Adds an item with a specific count (default 1) to the database, if there are
        no records of this user having that item yet, it will just add a record with quantity=quantity.
        :param item:
        :param quantity:
        :return:
        """

        query = """
        INSERT INTO inventory (user_id, item_id, quantity)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE quantity = quantity + %s;
        """

        database.execute_query(
            query,
            (self.user_id, item.id, abs(quantity), abs(quantity)),
        )

    def take_item(self, item: item_service.Item, quantity=1):
        query = """
        INSERT INTO inventory (user_id, item_id, quantity)
        VALUES (%s, %s, 0)
        ON DUPLICATE KEY UPDATE quantity = CASE
            WHEN quantity - %s < 0 THEN 0
            ELSE quantity - %s
        END;
        """

        database.execute_query(
            query,
            (self.user_id, item.id, self.user_id, item.id, abs(quantity)),
        )

    def get_inventory(self):
        query = "SELECT item_id, quantity FROM inventory WHERE user_id = %s AND quantity > 0"
        results = database.select_query(query, (self.user_id,))

        items_dict = {}
        for row in results:
            item_id, quantity = row
            item = item_service.Item(item_id)
            items_dict[item] = quantity

        return items_dict

    def get_item_quantity(self, item: item_service.Item):
        query = "SELECT COALESCE(quantity, 0) FROM inventory WHERE user_id = %s AND item_id = %s"
        return database.select_query_one(query, (self.user_id, item.id))

    def get_sell_data(self):
        query = """
                SELECT item.display_name
                FROM inventory
                JOIN ShopItem ON inventory.item_id = ShopItem.item_id
                JOIN item ON inventory.item_id = item.id
                WHERE inventory.user_id = %s AND inventory.quantity > 0 AND ShopItem.worth > 0
                """

        try:
            results = database.select_query(query, (self.user_id,))
            return [item[0] for item in results]

        except Exception as e:
            logger.error(e)
            return []
