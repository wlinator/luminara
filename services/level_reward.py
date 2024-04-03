from datetime import datetime, timedelta
from db import database

import pytz

from config.parser import JsonCache

resources = JsonCache.read_json("resources")


class LevelReward:
    def __init__(self, guild_id):
        self.guild_id = guild_id
        self.rewards = sorted(self.get_rewards())

    def get_rewards(self) -> dict:
        query = """
                SELECT level, role_id, persistent
                FROM level_rewards
                WHERE guild_id = %s
                """
        data = database.select_query(query, (self.guild_id,))

        rewards = {}
        for row in data:
            rewards[int(row[0])] = [int(row[1]), row[2]]

        return rewards

    def level_role(self, level: int):
        if self.rewards:
            if level in self.rewards:
                return self.rewards[level][0]

        return None

    def replace_previous(self, level) -> bool:
        index = self.rewards.index(level)

        if index != 0:
            previous_key = self.rewards[index - 1]
            return not bool(self.rewards[previous_key][1])

        return False
