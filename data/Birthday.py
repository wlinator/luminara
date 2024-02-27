import datetime

import pytz

from db import database


class Birthday:
    def __init__(self, user_id):
        self.user_id = user_id

    def set(self, birthday):
        query = """
                INSERT INTO birthdays (user_id, birthday)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE birthday = VALUES(birthday);
                """

        database.execute_query(query, (self.user_id, birthday))

    @staticmethod
    def today():
        query = """
                SELECT user_id
                FROM birthdays
                WHERE DATE_FORMAT(birthday, '%m-%d') = %s
                """

        tz = pytz.timezone('US/Eastern')
        date = datetime.datetime.now(tz).strftime("%m-%d")

        ids = database.select_query(query, (date,))
        ids = [item[0] for item in ids]

        return ids
