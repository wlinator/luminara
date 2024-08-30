from datetime import UTC, datetime
from typing import Any

from db import database


class CustomReactionsService:
    def __init__(self):
        pass

    async def find_trigger(
        self,
        guild_id: int,
        message_content: str,
    ) -> dict[str, Any] | None:
        message_content = message_content.lower()
        query = """
        SELECT * FROM custom_reactions
        WHERE (guild_id = %s OR is_global = TRUE) AND (
            (is_full_match = TRUE AND trigger_text = %s) OR
            (is_full_match = FALSE AND %s LIKE CONCAT('%%', trigger_text, '%%'))
        )
        ORDER BY guild_id = %s DESC, is_global ASC
        LIMIT 1
        """
        if result := database.select_query(
            query,
            (guild_id, message_content, message_content, guild_id),
        ):
            reaction = result[0]  # Get the first result from the list
            return {
                "id": reaction[0],
                "trigger_text": reaction[1],
                "response": reaction[2],
                "emoji_id": reaction[3],
                "is_emoji": reaction[4],
                "is_full_match": reaction[5],
                "is_global": reaction[6],
                "guild_id": reaction[7],
                "creator_id": reaction[8],
                "usage_count": reaction[9],
                "created_at": reaction[10],
                "updated_at": reaction[11],
                "type": "emoji" if reaction[4] else "text",
            }
        return None

    async def find_id(self, reaction_id: int) -> dict[str, Any] | None:
        query = """
        SELECT * FROM custom_reactions
        WHERE id = %s
        LIMIT 1
        """
        if result := database.select_query(query, (reaction_id,)):
            reaction = result[0]  # Get the first result from the list
            return {
                "id": reaction[0],
                "trigger_text": reaction[1],
                "response": reaction[2],
                "emoji_id": reaction[3],
                "is_emoji": reaction[4],
                "is_full_match": reaction[5],
                "is_global": reaction[6],
                "guild_id": reaction[7],
                "creator_id": reaction[8],
                "usage_count": reaction[9],
                "created_at": reaction[10],
                "updated_at": reaction[11],
                "type": "emoji" if reaction[4] else "text",
            }
        return None

    async def find_all_by_guild(self, guild_id: int) -> list[dict[str, Any]]:
        query = """
        SELECT * FROM custom_reactions
        WHERE guild_id = %s
        """
        results = database.select_query(query, (guild_id,))
        return [
            {
                "id": reaction[0],
                "trigger_text": reaction[1],
                "response": reaction[2],
                "emoji_id": reaction[3],
                "is_emoji": reaction[4],
                "is_full_match": reaction[5],
                "is_global": reaction[6],
                "guild_id": reaction[7],
                "creator_id": reaction[8],
                "usage_count": reaction[9],
                "created_at": reaction[10],
                "updated_at": reaction[11],
                "type": "emoji" if reaction[4] else "text",
            }
            for reaction in results
        ]

    async def create_custom_reaction(
        self,
        guild_id: int,
        creator_id: int,
        trigger_text: str,
        response: str | None = None,
        emoji_id: int | None = None,
        is_emoji: bool = False,
        is_full_match: bool = False,
        is_global: bool = True,
    ) -> bool:
        if await self.count_custom_reactions(guild_id) >= 100:
            return False

        query = """
        INSERT INTO custom_reactions (trigger_text, response, emoji_id, is_emoji, is_full_match, is_global, guild_id, creator_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE trigger_text=trigger_text
        """
        database.execute_query(
            query,
            (
                trigger_text,
                response,
                emoji_id,
                is_emoji,
                is_full_match,
                is_global,
                guild_id,
                creator_id,
            ),
        )
        return True

    async def edit_custom_reaction(
        self,
        reaction_id: int,
        new_response: str | None = None,
        new_emoji_id: int | None = None,
        is_emoji: bool | None = None,
        is_full_match: bool | None = None,
        is_global: bool | None = None,
    ) -> bool:
        query = """
        UPDATE custom_reactions
        SET response = COALESCE(%s, response),
            emoji_id = COALESCE(%s, emoji_id),
            is_emoji = COALESCE(%s, is_emoji),
            is_full_match = COALESCE(%s, is_full_match),
            is_global = COALESCE(%s, is_global),
            updated_at = %s
        WHERE id = %s
        """
        database.execute_query(
            query,
            (
                new_response,
                new_emoji_id,
                is_emoji,
                is_full_match,
                is_global,
                datetime.now(UTC),
                reaction_id,
            ),
        )
        return True

    async def delete_custom_reaction(self, reaction_id: int) -> bool:
        query = """
        DELETE FROM custom_reactions
        WHERE id = %s
        """
        database.execute_query(query, (reaction_id,))
        return True

    async def count_custom_reactions(self, guild_id: int) -> int:
        query = """
        SELECT COUNT(*) FROM custom_reactions
        WHERE guild_id = %s
        """
        count = database.select_query_one(query, (guild_id,))
        return count or 0

    async def increment_reaction_usage(self, reaction_id: int) -> bool:
        query = """
        UPDATE custom_reactions
        SET usage_count = usage_count + 1
        WHERE id = %s
        """
        database.execute_query(
            query,
            (reaction_id,),
        )
        return True
