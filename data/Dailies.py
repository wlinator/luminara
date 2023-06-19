import json
import time

from db import database

with open("json/economy.json") as file:
    json_data = json.load(file)


class Dailies:
    def __init__(self, user_id, claimed_at, next_available):
        self.user_id = user_id
        self.amount = json_data["daily_reward"]
        self.claimed_at = claimed_at
        self.next_available = next_available

    def push(self):
        query = """
        INSERT INTO dailies (user_id, amount, claimed_at, next_available)
        VALUES (?, ?, ?, ?)
        """

        values = (self.user_id, self.amount, self.claimed_at, self.next_available)

        database.execute_query(query, values)

    @staticmethod
    def cooldown_check(user_id):
        query = """
        SELECT next_available
        FROM dailies
        WHERE id = (
            SELECT MAX(id)
            FROM dailies
            WHERE user_id = ?
        )
        """

        values = (user_id,)
        result = database.select_query_one(query, values)
        current_time = time.time()

        if result and current_time < result:
            return False, result

        return True, result
