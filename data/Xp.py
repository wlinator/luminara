import os
import random
import time

from dotenv import load_dotenv

from db import database
from sb_tools import xp_functions

load_dotenv('.env')


class Xp:

    @staticmethod
    def get_user_xp_data(user_id):
        query = "SELECT user_xp, user_level, cooldown FROM xp WHERE user_id = {}".format(user_id)
        data = database.select_query(query)

        if data:
            return data
        else:
            Xp.create_new_user_xp(user_id)
            return [(3, 0, time.time())]

    @staticmethod
    def update_user_xp(user_id, new_xp, new_level, new_cooldown):
        query = "UPDATE xp SET user_xp = {}, user_level = {}, cooldown = {} WHERE user_id = {}" \
            .format(new_xp, new_level, new_cooldown, user_id)
        database.execute_query(query)

    @staticmethod
    def create_new_user_xp(user_id):
        query = "INSERT INTO xp(user_id, user_xp, user_level, cooldown) VALUES ({}, 3, 0, {})".format(user_id,
                                                                                                      time.time())
        database.execute_query(query)
        print(f"XP UPDATE --- USER with ID {user_id} started leveling (db_lvl_null)")

    @staticmethod
    def calculate_rank(user_id):
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
            if entry[0] == user_id:
                user_rank = entry[3]
                break

        return user_rank

    @staticmethod
    async def assign_level_role(user, level):

        level_roles = {
            "level_5": 1118491431036792922,
            "level_10": 1118491486259003403,
            "level_15": 1118491512536301570,
            "level_20": 1118491532111126578,
            "level_25": 1118491554005393458,
            "level_30": 1118491572770713710,
            "level_35": 1118491596820840492,
            "level_40": 1118491622045405287,
            "level_45": 1118491650721853500,
            "level_50": 1118491681004732466,
            # Add more level roles as needed
        }

        guild = user.guild
        current_level_role = None
        new_level_role_id = level_roles.get(f"level_{level}")

        for role in user.roles:
            if role.id in level_roles.values() and role.id != new_level_role_id:
                current_level_role = role
                break

        new_level_role = guild.get_role(new_level_role_id)
        await user.add_roles(new_level_role)

        if current_level_role:
            await user.remove_roles(current_level_role)

        return new_level_role_id

    @staticmethod
    def generate_progress_bar(current_value, target_value, bar_length=10):
        progress = current_value / target_value
        filled_length = int(bar_length * progress)
        empty_length = bar_length - filled_length
        bar = "▰" * filled_length + "▱" * empty_length
        return f"`{bar}` {current_value}/{target_value}"

    @staticmethod
    def load_leaderboard():
        query = "SELECT user_id, user_xp, user_level FROM xp ORDER BY user_level DESC, user_xp DESC"
        data = database.select_query(query)

        leaderboard = []
        rank = 1
        for row in data:
            row_user_id = row[0]
            user_xp = row[1]
            user_level = row[2]
            needed_xp_for_next_level = xp_functions.xp_needed_for_next_level(user_level)
            leaderboard.append((row_user_id, user_xp, user_level, rank, needed_xp_for_next_level))
            rank += 1

        return leaderboard

    @staticmethod
    def load_gain_data():
        xp_gain = list(map(int, os.getenv("XP_GAIN").split(",")))
        cooldown = list(map(int, os.getenv("COOLDOWN").split(",")))

        return random.choice(xp_gain), random.choice(cooldown)
