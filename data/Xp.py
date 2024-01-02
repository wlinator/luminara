import os
import random
import time

from dotenv import load_dotenv

from db import database

load_dotenv('.env')


class Xp:
    """
    Stores and retrieves XP from the database for a given user.
    """
    def __init__(self, user_id):
        self.user_id = user_id
        self.xp = None
        self.level = None
        self.ctime = None
        self.xp_gain = None
        self.new_cooldown = None

        self.fetch_or_create_xp()
        self.load_gain_data()

    def push(self):
        """
        Updates the XP and cooldown for a user.
        """
        query = """
                UPDATE xp
                SET user_xp = %s, user_level = %s, cooldown = %s
                WHERE user_id = %s
                """
        database.execute_query(query, (self.xp, self.level, self.ctime, self.user_id))

    def fetch_or_create_xp(self):
        """
        Gets a user's XP from the database or inserts a new row if it doesn't exist yet.
        """
        query = "SELECT user_xp, user_level, cooldown FROM xp WHERE user_id = %s"

        try:
            (user_xp, user_level, cooldown) = database.select_query(query, (self.user_id,))[0]
        except (IndexError, TypeError):
            (user_xp, user_level, cooldown) = (None, None, None)

        if any(var is None for var in [user_xp, user_level, cooldown]):
            query = """
                    INSERT INTO xp (user_id, user_xp, user_level, cooldown)
                    VALUES (%s, 0, 0, %s)
                    """
            database.execute_query(query, (self.user_id, time.time()))
            (user_xp, user_level, cooldown) = (0, 0, time.time())

        self.xp = user_xp
        self.level = user_level
        self.ctime = cooldown

    def load_gain_data(self):
        """
        Returns all values needed to calculate XP gain per message.

        - xp_gain = a random number from an env var list
        - cooldown = time in seconds
        """
        xp_gain = list(map(int, os.getenv("XP_GAIN").split(",")))
        cooldown = list(map(int, os.getenv("COOLDOWN").split(",")))

        self.xp_gain = random.choice(xp_gain)
        self.new_cooldown = random.choice(cooldown)

    def calculate_rank(self):
        """
        Checks which rank a user is, globally
        """
        query = "SELECT user_id, user_xp, user_level FROM xp ORDER BY user_level DESC, user_xp DESC"
        data = database.select_query(query)

        leaderboard = []
        rank = 1
        for row in data:
            row_user_id = row[0]
            user_xp = row[1]
            user_level = row[2]
            leaderboard.append((row_user_id, user_xp, user_level, rank))
            rank += 1

        user_rank = None
        for entry in leaderboard:
            if entry[0] == self.user_id:
                user_rank = entry[3]
                break

        return user_rank

    @staticmethod
    def load_leaderboard():
        """
        Returns the global XP leaderboard
        """
        query = "SELECT user_id, user_xp, user_level FROM xp ORDER BY user_level DESC, user_xp DESC"
        data = database.select_query(query)

        leaderboard = []
        rank = 1
        for row in data:
            row_user_id = row[0]
            user_xp = row[1]
            user_level = row[2]
            needed_xp_for_next_level = Xp.xp_needed_for_next_level(user_level)
            leaderboard.append((row_user_id, user_xp, user_level, rank, needed_xp_for_next_level))
            rank += 1

        return leaderboard

    @staticmethod
    def generate_progress_bar(current_value, target_value, bar_length=10):
        """
        Generates an XP progress bar based on the current level and XP.
        """
        progress = current_value / target_value
        filled_length = int(bar_length * progress)
        empty_length = bar_length - filled_length
        bar = "▰" * filled_length + "▱" * empty_length
        return f"`{bar}` {current_value}/{target_value}"

    @staticmethod
    def xp_needed_for_next_level(current_level):
        """
        Calculates the amount of XP needed to go to the next level, based on the current level.
        """
        formula_mapping = {
            (10, 19): lambda level: 12 * level + 27,
            (20, 29): lambda level: 15 * level + 27,
            (30, 39): lambda level: 18 * level + 27,
            (40, 49): lambda level: 21 * level + 27,
            (50, 59): lambda level: 24 * level + 27,
            (60, 69): lambda level: 27 * level + 27,
            (70, 79): lambda level: 30 * level + 27,
            (80, 89): lambda level: 33 * level + 27,
            (90, 99): lambda level: 36 * level + 27,
            (100, 109): lambda level: 39 * level + 27,
        }

        for level_range, formula in formula_mapping.items():
            if level_range[0] <= current_level <= level_range[1]:
                return formula(current_level)

        # For levels below 10 and levels 110 and above
        return 9 * current_level + 27 if current_level < 30 else 42 * current_level + 27
