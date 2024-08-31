import datetime

import pytz

from db import database


class Birthday:
    def __init__(self, user_id: int, guild_id: int) -> None:
        self.user_id: int = user_id
        self.guild_id: int = guild_id

    def set(self, birthday: datetime.date) -> None:
        query: str = """
                INSERT INTO birthdays (user_id, guild_id, birthday)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE birthday = VALUES(birthday);
                """

        database.execute_query(query, (self.user_id, self.guild_id, birthday))

    def delete(self) -> None:
        query: str = """
                DELETE FROM birthdays
                WHERE user_id = %s AND guild_id = %s;
                """

        database.execute_query(query, (self.user_id, self.guild_id))

    @staticmethod
    def get_birthdays_today() -> list[tuple[int, int]]:
        query: str = """
                SELECT user_id, guild_id
                FROM birthdays
                WHERE DATE_FORMAT(birthday, '%m-%d') = %s
                """

        tz = pytz.timezone("US/Eastern")
        today: str = datetime.datetime.now(tz).strftime("%m-%d")

        return database.select_query(query, (today,))

    @staticmethod
    def get_upcoming_birthdays(guild_id: int) -> list[tuple[int, str]]:
        query: str = """
                SELECT user_id, DATE_FORMAT(birthday, '%m-%d') AS upcoming_birthday 
                FROM birthdays 
                WHERE guild_id = %s 
                ORDER BY (DAYOFYEAR(birthday) - DAYOFYEAR(now()) + 366) % 366;
                """

        data: list[tuple[int, str]] = database.select_query(query, (guild_id,))

        return [(int(row[0]), str(row[1])) for row in data]
