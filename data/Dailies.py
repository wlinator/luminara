import json
from datetime import datetime, timedelta

import pytz

from data.Currency import Currency
from db import database

with open("json/economy.json") as file:
    json_data = json.load(file)


class Dailies:
    def __init__(self, user_id):
        self.user_id = user_id
        self.amount = json_data["daily_reward"]
        self.tz = pytz.timezone('US/Eastern')

        data = Dailies.get_data(user_id)

        if data[0] is not None:
            self.claimed_at = datetime.fromisoformat(data[0])
        else:
            # set date as yesterday to pretend as a valid claimed_at.
            self.claimed_at = datetime.now(tz=self.tz) - timedelta(days=2)
            print(self.claimed_at)

        self.streak = int(data[1])

    def refresh(self):
        if self.streak_check():
            self.streak += 1
        else:
            self.streak = 1

        self.claimed_at = datetime.now(tz=self.tz).isoformat()

        query = """
        INSERT INTO dailies (user_id, amount, claimed_at, streak)
        VALUES (?, ?, ?, ?)
        """
        values = (self.user_id, self.amount, self.claimed_at, self.streak)
        database.execute_query(query, values)

        cash = Currency(self.user_id)
        cash.add_cash(self.amount)
        cash.push()

    def can_be_claimed(self):
        if self.claimed_at is None:
            return True

        else:
            time_now = datetime.now(tz=self.tz)
            reset_time = time_now.replace(hour=7, minute=0, second=0, microsecond=0)

            if time_now < reset_time:
                reset_time -= timedelta(days=1)

            if self.claimed_at < reset_time <= time_now:
                return True

        return False

    def streak_check(self):
        yesterday = datetime.now(tz=self.tz) - timedelta(days=1)
        return self.claimed_at.date() == yesterday.date()

    @staticmethod
    def get_data(user_id):
        query = """
        SELECT claimed_at, streak 
        FROM dailies 
        WHERE id = (
            SELECT MAX(id)
            FROM dailies
            WHERE user_id = ?
        )
        """

        try:
            (claimed_at, streak) = database.select_query(query, (user_id,))[0]
        except (IndexError, TypeError):
            (claimed_at, streak) = None, 0

        return claimed_at, streak
