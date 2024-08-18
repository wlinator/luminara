import time
from typing import Callable, Dict, List, Optional, Tuple

from discord.ext import commands

from db import database
from lib.constants import CONST


class XpService:
    """
    Manages XP for a user, including storing, retrieving, and updating XP in the database.
    """

    def __init__(self, user_id: int, guild_id: int) -> None:
        """
        Initializes the XpService with user and guild IDs, and fetches or creates XP data.

        Args:
            user_id (int): The ID of the user.
            guild_id (int): The ID of the guild.
        """
        self.user_id: int = user_id
        self.guild_id: int = guild_id
        self.xp: int = 0
        self.level: int = 0
        self.cooldown_time: Optional[float] = None
        self.xp_gain: int = CONST.XP_GAIN_PER_MESSAGE
        self.new_cooldown: int = CONST.XP_GAIN_COOLDOWN

        self.fetch_or_create_xp()

    def push(self) -> None:
        """
        Updates the XP and cooldown for a user in the database.
        """
        query: str = """
                UPDATE xp
                SET user_xp = %s, user_level = %s, cooldown = %s
                WHERE user_id = %s AND guild_id = %s
                """
        database.execute_query(
            query,
            (self.xp, self.level, self.cooldown_time, self.user_id, self.guild_id),
        )

    def fetch_or_create_xp(self) -> None:
        """
        Retrieves a user's XP from the database or inserts a new row if it doesn't exist yet.
        """
        query: str = "SELECT user_xp, user_level, cooldown FROM xp WHERE user_id = %s AND guild_id = %s"

        try:
            user_xp, user_level, cooldown = database.select_query(
                query,
                (self.user_id, self.guild_id),
            )[0]
        except (IndexError, TypeError):
            user_xp, user_level, cooldown = 0, 0, None

        if any(var is None for var in [user_xp, user_level, cooldown]):
            query = """
                    INSERT INTO xp (user_id, guild_id, user_xp, user_level, cooldown)
                    VALUES (%s, %s, 0, 0, %s)
                    """
            database.execute_query(query, (self.user_id, self.guild_id, time.time()))
            user_xp, user_level, cooldown = 0, 0, time.time()

        self.xp = user_xp
        self.level = user_level
        self.cooldown_time = cooldown

    def calculate_rank(self) -> Optional[int]:
        """
        Determines the rank of a user in the guild based on their XP and level.

        Returns:
            Optional[int]: The rank of the user in the guild, or None if not found.
        """
        query: str = """
                SELECT user_id, user_xp, user_level
                FROM xp 
                WHERE guild_id = %s
                ORDER BY user_level DESC, user_xp DESC
                """
        data: List[Tuple[int, int, int]] = database.select_query(
            query,
            (self.guild_id,),
        )

        leaderboard: List[Tuple[int, int, int, int]] = [
            (row[0], row[1], row[2], rank) for rank, row in enumerate(data, start=1)
        ]
        return next(
            (entry[3] for entry in leaderboard if entry[0] == self.user_id),
            None,
        )

    @staticmethod
    def load_leaderboard(guild_id: int) -> List[Tuple[int, int, int, int]]:
        """
        Retrieves the guild's XP leaderboard.

        Args:
            guild_id (int): The ID of the guild.

        Returns:
            List[Tuple[int, int, int, int]]: A list of tuples containing user_id, user_xp, user_level, and needed_xp_for_next_level.
        """
        query: str = """
                SELECT user_id, user_xp, user_level 
                FROM xp 
                WHERE guild_id = %s
                ORDER BY user_level DESC, user_xp DESC
                """
        data: List[Tuple[int, int, int]] = database.select_query(query, (guild_id,))

        leaderboard: List[Tuple[int, int, int, int]] = []
        for row in data:
            row_user_id: int = row[0]
            user_xp: int = row[1]
            user_level: int = row[2]
            needed_xp_for_next_level: int = XpService.xp_needed_for_next_level(
                user_level,
            )

            leaderboard.append(
                (row_user_id, user_xp, user_level, needed_xp_for_next_level),
            )

        return leaderboard

    @staticmethod
    def generate_progress_bar(
            current_value: int,
            target_value: int,
            bar_length: int = 10,
    ) -> str:
        """
        Generates an XP progress bar based on the current level and XP.

        Args:
            current_value (int): The current XP value.
            target_value (int): The target XP value.
            bar_length (int, optional): The length of the progress bar. Defaults to 10.

        Returns:
            str: The formatted progress bar.
        """
        progress: float = current_value / target_value
        filled_length: int = int(bar_length * progress)
        empty_length: int = bar_length - filled_length
        bar: str = "▰" * filled_length + "▱" * empty_length
        return f"`{bar}` {current_value}/{target_value}"

    @staticmethod
    def xp_needed_for_next_level(current_level: int) -> int:
        """
        Calculates the amount of XP needed to reach the next level, based on the current level.

        Args:
            current_level (int): The current level of the user.

        Returns:
            int: The amount of XP needed for the next level.
        """
        formula_mapping: Dict[Tuple[int, int], Callable[[int], int]] = {
            (10, 19): lambda level: 12 * level + 28,
            (20, 29): lambda level: 15 * level + 29,
            (30, 39): lambda level: 18 * level + 30,
            (40, 49): lambda level: 21 * level + 31,
            (50, 59): lambda level: 24 * level + 32,
            (60, 69): lambda level: 27 * level + 33,
            (70, 79): lambda level: 30 * level + 34,
            (80, 89): lambda level: 33 * level + 35,
            (90, 99): lambda level: 36 * level + 36,
        }

        return next(
            (
                formula(current_level)
                for level_range, formula in formula_mapping.items()
                if level_range[0] <= current_level <= level_range[1]
            ),
            (
                10 * current_level + 27
                if current_level < 10
                else 42 * current_level + 37
            ),
        )


class XpRewardService:
    """
    Manages XP rewards for a guild, including storing, retrieving, and updating rewards in the database.
    """

    def __init__(self, guild_id: int) -> None:
        """
        Initializes the XpRewardService with the guild ID and fetches rewards.

        Args:
            guild_id (int): The ID of the guild.
        """
        self.guild_id: int = guild_id
        self.rewards: Dict[int, Tuple[int, bool]] = self._fetch_rewards()

    def _fetch_rewards(self) -> Dict[int, Tuple[int, bool]]:
        """
        Retrieves the XP rewards for the guild from the database.

        Returns:
            Dict[int, Tuple[int, bool]]: A dictionary of rewards with levels as keys and (role_id, persistent) as values.
        """
        query: str = """
                SELECT level, role_id, persistent
                FROM level_rewards
                WHERE guild_id = %s
                ORDER BY level DESC
                """
        data: List[Tuple[int, int, bool]] = database.select_query(
            query,
            (self.guild_id,),
        )
        return {level: (role_id, persistent) for level, role_id, persistent in data}

    def add_reward(self, level: int, role_id: int, persistent: bool) -> None:
        """
        Adds a new XP reward for the guild.

        Args:
            level (int): The level at which the reward is given.
            role_id (int): The ID of the role to be awarded.
            persistent (bool): Whether the reward is persistent.

        Raises:
            commands.BadArgument: If the server has more than 25 XP rewards.
        """
        if len(self.rewards) >= 25:
            raise commands.BadArgument("A server can't have more than 25 XP rewards.")

        query: str = """
                INSERT INTO level_rewards (guild_id, level, role_id, persistent)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE role_id = %s, persistent = %s;
                """
        database.execute_query(
            query,
            (self.guild_id, level, role_id, persistent, role_id, persistent),
        )
        self.rewards[level] = (role_id, persistent)

    def remove_reward(self, level: int) -> None:
        """
        Removes an XP reward for the guild.

        Args:
            level (int): The level at which the reward is to be removed.
        """
        query: str = """
                DELETE FROM level_rewards
                WHERE guild_id = %s AND level = %s;
                """
        database.execute_query(query, (self.guild_id, level))
        self.rewards.pop(level, None)

    def get_role(self, level: int) -> Optional[int]:
        """
        Retrieves the role ID for a given level.

        Args:
            level (int): The level for which to retrieve the role ID.

        Returns:
            Optional[int]: The role ID if found, otherwise None.
        """
        return self.rewards.get(level, (None,))[0]

    def should_replace_previous_reward(self, level: int) -> Tuple[Optional[int], bool]:
        """
        Checks if the previous reward should be replaced based on the given level.

        Args:
            level (int): The level to check for replacement.

        Returns:
            Tuple[Optional[int], bool]: A tuple containing the previous reward and a boolean indicating if it should be replaced.
        """
        previous_reward, replace = None, False
        if levels_below := [lvl for lvl in sorted(self.rewards) if lvl < level]:
            highest_level_below = max(levels_below)
            previous_reward, persistent = self.rewards[highest_level_below]
            replace = not persistent

        return previous_reward, replace
