import datetime

import pytz

from db import database


class Birthday:
    def __init__(self, user_id, guild_id):
        self.user_id = user_id
        self.guild_id = guild_id

    def set(self, birthday):
        query = """
                INSERT INTO birthdays (user_id, guild_id, birthday)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE birthday = VALUES(birthday);
                """

        database.execute_query(query, (self.user_id, self.guild_id, birthday))

    @staticmethod
    def get_birthdays_today():
        query = """
                SELECT user_id, guild_id
                FROM birthdays
                WHERE DATE_FORMAT(birthday, '%m-%d') = %s
                """

        tz = pytz.timezone("US/Eastern")
        today = datetime.datetime.now(tz).strftime("%m-%d")

        birthdays = database.select_query(query, (today,))

        return birthdays

    @staticmethod
    def get_upcoming_birthdays(guild_id):
        query = """
                SELECT user_id, DATE_FORMAT(birthday, '%m-%d') AS upcoming_birthday
                FROM birthdays
                WHERE DAYOFYEAR(birthday) > DAYOFYEAR(NOW())
                    AND guild_id = %s
                ORDER BY DAYOFYEAR(birthday);
                """
        data = database.select_query(query, (guild_id,))

        upcoming = []
        for row in data:
            user_id = row[0]
            birthday = row[1]
            upcoming.append((user_id, birthday))

        return upcoming

