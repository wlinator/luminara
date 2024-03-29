from datetime import datetime, timedelta

import pytz

from config.parser import JsonCache
from db import database
from services.Currency import Currency

resources = JsonCache.read_json("resources")


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
            self.amount = resources["daily_reward"]

        query = """
        INSERT INTO dailies (user_id, amount, claimed_at, streak)
        VALUES (%s, %s, %s, %s)
        """
        values = (self.user_id, self.amount, self.claimed_at, self.streak)
        database.execute_query(query, values)

        cash = Currency(self.user_id)
        cash.add_balance(self.amount)
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
            WHERE user_id = %s
        )
        """

        try:
            (claimed_at, streak) = database.select_query(query, (user_id,))[0]
        except (IndexError, TypeError):
            (claimed_at, streak) = None, 0

        return claimed_at, streak

    @staticmethod
    def load_leaderboard():
        query = """
                SELECT user_id, MAX(streak), claimed_at
                FROM dailies
                GROUP BY user_id
                ORDER BY MAX(streak) DESC;
                """

        data = database.select_query(query)

        leaderboard = []
        rank = 1
        for row in data:
            row_user_id = row[0]
            streak = row[1]
            claimed_at = row[2]
            leaderboard.append((row_user_id, streak, claimed_at, rank))
            rank += 1

        return leaderboard
