from datetime import datetime, timedelta

import pytz

from db import database
from lib.const import CONST
from services.currency_service import Currency


class Dailies:
    def __init__(self, user_id: int) -> None:
        self.user_id: int = user_id
        self.amount: int = 0
        self.tz = pytz.timezone("US/Eastern")
        self.time_now: datetime = datetime.now(tz=self.tz)
        self.reset_time: datetime = self.time_now.replace(
            hour=7,
            minute=0,
            second=0,
            microsecond=0,
        )

        data: tuple[str | None, int] = Dailies.get_data(user_id)

        if data[0] is not None:
            self.claimed_at: datetime = datetime.fromisoformat(data[0])
        else:
            # set date as yesterday to mock a valid claimed_at.
            self.claimed_at: datetime = datetime.now(tz=self.tz) - timedelta(days=2)

        self.streak: int = int(data[1])

    def refresh(self) -> None:
        if self.amount == 0:
            self.amount = CONST.DAILY_REWARD
        query: str = """
        INSERT INTO dailies (user_id, amount, claimed_at, streak)
        VALUES (%s, %s, %s, %s)
        """
        values: tuple[int, int, str, int] = (
            self.user_id,
            self.amount,
            self.claimed_at.isoformat(),
            self.streak,
        )
        database.execute_query(query, values)

        cash = Currency(self.user_id)
        cash.add_balance(self.amount)
        cash.push()

    def can_be_claimed(self) -> bool:
        if self.time_now < self.reset_time:
            self.reset_time -= timedelta(days=1)

        return self.claimed_at < self.reset_time <= self.time_now

    def streak_check(self) -> bool:
        """
        Three checks are performed, only one has to return True.
        1. the daily was claimed yesterday
        2. the daily was claimed the day before yesterday (users no longer lose their dailies as fast)
        3. the daily was claimed today but before the reset time (see __init__)
        :return:
        """

        check_1: bool = self.claimed_at.date() == (self.time_now - timedelta(days=1)).date()
        check_2: bool = self.claimed_at.date() == (self.time_now - timedelta(days=2)).date()
        check_3: bool = self.claimed_at.date() == self.time_now.date() and self.claimed_at < self.reset_time

        return check_1 or check_2 or check_3

    @staticmethod
    def get_data(user_id: int) -> tuple[str | None, int]:
        query: str = """
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
    def load_leaderboard() -> list[tuple[int, int, str, int]]:
        query: str = """
                SELECT user_id, MAX(streak), claimed_at
                FROM dailies
                GROUP BY user_id
                ORDER BY MAX(streak) DESC;
                """

        data: list[tuple[int, int, str]] = database.select_query(query)

        leaderboard: list[tuple[int, int, str, int]] = [
            (row[0], row[1], row[2], rank) for rank, row in enumerate(data, start=1)
        ]
        return leaderboard
