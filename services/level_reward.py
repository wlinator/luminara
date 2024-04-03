from datetime import datetime, timedelta
from db import database
from discord.ext import commands
import logging

from config.parser import JsonCache

resources = JsonCache.read_json("resources")
_logs = logging.getLogger('Racu.Core')


class LevelReward:
    def __init__(self, guild_id):
        self.guild_id = guild_id
        self.rewards = self.get_rewards()

    def get_rewards(self) -> dict:
        query = """
                SELECT level, role_id, persistent
                FROM level_rewards
                WHERE guild_id = %s
                ORDER BY level DESC
                """
        data = database.select_query(query, (self.guild_id,))

        rewards = {}
        for row in data:
            rewards[int(row[0])] = [int(row[1]), bool(row[2])]

        _logs.info(rewards)
        return rewards

    def add_reward(self, level: int, role_id: int, persistent: bool):
        query = """
                INSERT INTO level_rewards (guild_id, level, role_id, persistent)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE role_id = %s, persistent = %s;
                """

        database.execute_query(query, (self.guild_id, level, role_id, persistent, role_id, persistent))

    def remove_reward(self, level: int):
        query = """
                DELETE FROM level_rewards
                WHERE guild_id = %s
                AND level = %s;
                """

        database.execute_query(query, (self.guild_id, level))

    def role(self, level: int):
        if self.rewards:

            if level in self.rewards:
                role_id = self.rewards.get(level)[0]
                _logs.info(role_id)
                return role_id

        return None

    def replace_previous_reward(self, level):
        replace = False
        previous_reward = None
        levels = sorted(self.rewards.keys())

        if level in levels:
            values_below = [x for x in levels if x < level]

            if values_below:
                replace = not bool(self.rewards.get(max(values_below))[1])

            if replace:
                previous_reward = self.rewards.get(max(values_below))[0]

        return previous_reward, replace