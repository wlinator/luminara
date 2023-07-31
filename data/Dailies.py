import json
from datetime import datetime, timedelta

import pytz

from data.Currency import Currency
from db import database

with open("config/economy.json") as file:
    json_data = json.load(file)


class Dailies:
    def __init__(self, user_id):
        self.user_id = user_id
        self.amount = 0
        self.tz = pytz.timezone('US/Eastern')
        self.time_now = datetime.now(tz=self.tz)
        self.reset_time = self.time_now.replace(hour=7, minute=0, second=0, microsecond=0)

        data = Dailies.get_data(user_id)

        if data[0] is not None:
            self.claimed_at = datetime.fromisoformat(data[0])
        else:
            # set date as yesterday to pretend as a valid claimed_at.
            self.claimed_at = datetime.now(tz=self.tz) - timedelta(days=2)

        self.streak = int(data[1])

    def refresh(self):
        if self.amount == 0:
            self.amount = json_data["daily_reward"]

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

            if self.time_now < self.reset_time:
                self.reset_time -= timedelta(days=1)

            if self.claimed_at < self.reset_time <= self.time_now:
                return True

        return False

    def streak_check(self):
        """
        Three checks are performed, only one has to return True.
        1. the daily was claimed yesterday
        2. the daily was claimed the day before yesterday (users no longer lose their dailies as fast)
        3. the daily was claimed today but before the reset time (see __init__)
        :return:
        """

        check_1 = self.claimed_at.date() == (self.time_now - timedelta(days=1)).date()
        check_2 = self.claimed_at.date() == (self.time_now - timedelta(days=2)).date()
        check_3 = self.claimed_at.date() == self.time_now.date() and self.claimed_at < self.reset_time

        return check_1 or check_2 or check_3

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
