import json
import sqlite3

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
        WHERE id = ?
        """

        data = database.select_query(query, (self.id,))[0]
        return data

    def get_quantity(self, author_id):
        query = """
                SELECT COALESCE((SELECT quantity FROM inventory WHERE user_id = ? AND item_id = ?), 0) AS quantity
                """

        quantity = database.select_query_one(query, (author_id, self.id))

        return quantity

    @staticmethod
    def insert_items():
        with open("config/default_items.json", 'r') as file:
            items_data = json.load(file)

        for index, (item_id, item_data) in enumerate(items_data.items(), start=1):
            name = item_data["name"]
            display_name = item_data["display_name"]
            description = item_data["description"]
            image_url = item_data["image_url"]
            emote_id = item_data["emote_id"]
            quote = item_data["quote"]
            item_type = item_data["type"]

            query = """
                    INSERT OR REPLACE INTO item 
                    (id, name, display_name, description, image_url, emote_id, quote, type)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """
            database.execute_query(query,
                                   (index, name, display_name, description, image_url, emote_id, quote, item_type))

        print("Items inserted into the database successfully.")

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
            print(sqlite3.Error)
            return []

    @staticmethod
    def get_item_by_display_name(display_name):
        query = "SELECT id FROM item WHERE display_name = ?"
        item_id = database.select_query_one(query, (display_name,))
        return Item(item_id)

    @staticmethod
    def get_item_by_name(name):
        query = "SELECT id FROM item WHERE name = ?"
        item_id = database.select_query_one(query, (name,))
        return Item(item_id)