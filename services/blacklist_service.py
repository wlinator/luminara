from typing import List, Optional, Tuple

from db import database


class BlacklistUserService:
    def __init__(self, user_id: int) -> None:
        self.user_id: int = user_id

    def add_to_blacklist(self, reason: Optional[str] = None) -> None:
        """
        Adds a user to the blacklist with the given reason.

        Args:
            reason (str): The reason for blacklisting the user.
        """
        query: str = """
                INSERT INTO blacklist_user (user_id, reason)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE reason = VALUES(reason)
                """
        database.execute_query(query, (self.user_id, reason))

    @staticmethod
    def is_user_blacklisted(user_id: int) -> bool:
        """
        Checks if a user is currently blacklisted.

        Args:
            user_id (int): The ID of the user to check.

        Returns:
            bool: True if the user is blacklisted, False otherwise.
        """
        query: str = """
                SELECT active
                FROM blacklist_user
                WHERE user_id = %s
                """
        result: List[Tuple[bool]] = database.select_query(query, (user_id,))
        return any(active for (active,) in result)
