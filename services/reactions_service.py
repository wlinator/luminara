from typing import Optional, Dict, Any
from datetime import datetime
from db import database


class CustomReactionsService:
    def __init__(self):
        pass

    async def find_trigger(
        self, guild_id: int, message_content: str
    ) -> Optional[Dict[str, Any]]:
        message_content = message_content.lower()
        query = """
        SELECT * FROM custom_reactions
        WHERE (guild_id = ? OR is_global = TRUE) AND (
            (is_full_match = TRUE AND trigger_text = ?) OR
            (is_full_match = FALSE AND ? LIKE CONCAT('%', trigger_text, '%'))
        )
        ORDER BY guild_id = ? DESC, is_global ASC
        LIMIT 1
        """
        result = database.select_query(query, (guild_id, message_content, message_content, guild_id))
        if result:
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
                "type": "emoji" if reaction[4] else "text"
            }
        return None

    async def create_custom_reaction(
        self,
        guild_id: int,
        creator_id: int,
        trigger_text: str,
        response: Optional[str] = None,
        emoji_id: Optional[int] = None,
        is_emoji: bool = False,
        is_full_match: bool = False,
        is_global: bool = True,
    ) -> bool:
        if await self.count_custom_reactions(guild_id) >= 100:
            return False

        query = """
        INSERT INTO custom_reactions (trigger_text, response, emoji_id, is_emoji, is_full_match, is_global, guild_id, creator_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
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
        new_response: Optional[str] = None,
        new_emoji_id: Optional[int] = None,
        is_emoji: Optional[bool] = None,
        is_full_match: Optional[bool] = None,
        is_global: Optional[bool] = None,
    ) -> bool:
        query = """
        UPDATE custom_reactions
        SET response = COALESCE(?, response),
            emoji_id = COALESCE(?, emoji_id),
            is_emoji = COALESCE(?, is_emoji),
            is_full_match = COALESCE(?, is_full_match),
            is_global = COALESCE(?, is_global),
            updated_at = ?
        WHERE id = ?
        """
        database.execute_query(
            query,
            (
                new_response,
                new_emoji_id,
                is_emoji,
                is_full_match,
                is_global,
                datetime.utcnow(),
                reaction_id,
            ),
        )
        return True

    async def delete_custom_reaction(self, reaction_id: int) -> bool:
        query = """
        DELETE FROM custom_reactions
        WHERE id = ?
        """
        database.execute_query(query, (reaction_id,))
        return True

    async def count_custom_reactions(self, guild_id: int) -> int:
        query = """
        SELECT COUNT(*) FROM custom_reactions
        WHERE guild_id = ?
        """
        count = database.select_query_one(query, (guild_id,))
        return count if count else 0
    
    async def increment_reaction_usage(self, reaction_id: int) -> bool:
        query = """
        UPDATE custom_reactions
        SET usage_count = usage_count + 1
        WHERE id = ?
        """
        database.execute_query(
            query,
            (
                reaction_id,
            ),
        )
        return True
