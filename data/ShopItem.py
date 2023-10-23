from data.Item import Item
from db import database


class ShopItem:
    def __init__(self, item: Item):
        self.item = item
        self.price = None
        self.price_special = None
        self.worth = None
        self.description = None

        self.fetch_or_create_shopitem()

        """
        if either price, price_special or worth equal "0",
        this will be interpreted as no-buy or no-sell.
        """

    def set_price(self, price):
        query = "UPDATE ShopItem SET price = %s WHERE item_id = %s"
        database.execute_query(query, (price, self.item.id))
        self.price = price

    def set_price_special(self, price_special):
        query = "UPDATE ShopItem SET price_special = %s WHERE item_id = %s"
        database.execute_query(query, (price_special, self.item.id))
        self.price_special = price_special

    def set_worth(self, worth):
        query = "UPDATE ShopItem SET worth = %s WHERE item_id = %s"
        database.execute_query(query, (worth, self.item.id))
        self.worth = worth

    def set_description(self, description):
        query = "UPDATE ShopItem SET description = %s WHERE item_id = %s"
        database.execute_query(query, (description, self.item.id))
        self.description = description

    def fetch_or_create_shopitem(self):
        query = """
                SELECT price, price_special, worth, description
                FROM ShopItem
                WHERE item_id = %s
                """

        try:
            (price, price_special, worth, description) = database.select_query(query, (self.item.id,))[0]
        except (IndexError, TypeError):
            query = """
                                INSERT INTO ShopItem (item_id, price, price_special, worth, description)
                                VALUES (%s, 0, 0, 0, "placeholder_descr")
                                """
            database.execute_query(query, (self.item.id,))
            (price, price_special, worth, description) = 0, 0, 0, "placeholder_descr"

        self.price = price
        self.price_special = price_special
        self.worth = worth
        self.description = description

    @staticmethod
    def get_shop_all():
        query = "SELECT item_id FROM ShopItem WHERE price != 0 OR price_special != 0;"
        shop_items = database.select_query(query)
        shop_items = [item[0] for item in shop_items]

        list = []
        for item_id in shop_items:
            list.append(ShopItem(Item(item_id)))

        return list
