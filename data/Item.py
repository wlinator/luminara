import json

from db import database


class Item:
    def __init__(self, item_id):
        self.item_id = item_id

        data = self.get_item_data()
        print(data)

        self.id_name = data[0]
        self.display_name = data[1]
        self.description = data[2]
        self.image_url = data[3]
        self.emote_id = data[4]
        self.quote = data[5]
        self.type = data[6]

    def get_item_data(self):
        query = """
        SELECT id_name, display_name, description, image_url, emote_id, quote, type
        FROM item
        WHERE item_id = ?
        """

        return database.select_query(query, (self.item_id,))[0]

    @staticmethod
    def insert_items():
        with open("config/default_items.json", 'r') as file:
            items_data = json.load(file)

        for index, (item_id, item_data) in enumerate(items_data.items(), start=1):
            id_name = item_data["id_name"]
            display_name = item_data["display_name"]
            description = item_data["description"]
            image_url = item_data["image_url"]
            emote_id = item_data["emote_id"]
            quote = item_data["quote"]
            type = item_data["type"]

            query = """
            INSERT OR IGNORE INTO item 
            (item_id, id_name, display_name, description, image_url, emote_id, quote, type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            database.execute_query(query,
                                   (index, id_name, display_name, description, image_url, emote_id, quote, type))

        print("Items inserted into the database successfully.")
