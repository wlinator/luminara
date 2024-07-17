import sqlite3

from loguru import logger

from db import database


class Item:
    def __init__(self, item_id):
        self.id = item_id

        data = self.get_item_data()

        self.name = data[0]
        self.display_name = data[1]
        self.description = data[2]
        self.image_url = data[3]
        self.emote_id = data[4]
        self.quote = data[5]
        self.type = data[6]

    def get_item_data(self):
        query = """
        SELECT name, display_name, description, image_url, emote_id, quote, type
        FROM item
        WHERE id = %s
        """

        data = database.select_query(query, (self.id,))[0]
        return data

    def get_quantity(self, author_id):
        query = """
                SELECT COALESCE((SELECT quantity FROM inventory WHERE user_id = %s AND item_id = %s), 0) AS quantity
                """

        quantity = database.select_query_one(query, (author_id, self.id))

        return quantity

    def get_item_worth(self):
        query = """
                SELECT worth
                FROM ShopItem
                WHERE item_id = %s
                """

        return database.select_query_one(query, (self.id,))

    @staticmethod
    def get_all_item_names():
        query = "SELECT display_name FROM item"

        try:
            item_names = []
            items = database.select_query(query)

            for item in items:
                item_names.append(item[0])

            return item_names

        except sqlite3.Error:
            logger.error(sqlite3.Error)
            return []

    @staticmethod
    def get_item_by_display_name(display_name):
        query = "SELECT id FROM item WHERE display_name = %s"
        item_id = database.select_query_one(query, (display_name,))
        return Item(item_id)

    @staticmethod
    def get_item_by_name(name):
        query = "SELECT id FROM item WHERE name = %s"
        item_id = database.select_query_one(query, (name,))
        return Item(item_id)
