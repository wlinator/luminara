"""
TABLE custom_reactions:
    id SERIAL PRIMARY KEY
    trigger TEXT NOT NULL
    response TEXT
    emoji TEXT
    is_emoji BOOLEAN DEFAULT FALSE
    is_full_match BOOLEAN DEFAULT FALSE
    is_global BOOLEAN DEFAULT TRUE
    guild_id BIGINT
    creator_id BIGINT NOT NULL
    usage_count INT DEFAULT 0
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    CONSTRAINT unique_trigger_guild UNIQUE (trigger, guild_id)
"""

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
            (is_full_match = TRUE AND trigger = ?) OR
            (is_full_match = FALSE AND ? LIKE CONCAT('%', trigger, '%'))
        )
        ORDER BY guild_id = ? DESC, is_global ASC
        LIMIT 1
        """
        result = database.select_query_one(query, (guild_id, message_content, message_content, guild_id))
        if result:
            reaction = dict(result)
            return {
                "response": reaction.get("response"),
                "type": "emoji" if reaction.get("is_emoji") else "text"
            }
        return None

    async def create_custom_reaction(
        self,
        guild_id: int,
        creator_id: int,
        trigger: str,
        response: Optional[str] = None,
        emoji: Optional[str] = None,
        is_emoji: bool = False,
        is_full_match: bool = False,
        is_global: bool = True,
    ) -> bool:
        if await self.count_custom_reactions(guild_id) >= 100:
            return False

        query = """
        INSERT INTO custom_reactions (trigger, response, emoji, is_emoji, is_full_match, is_global, guild_id, creator_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON DUPLICATE KEY UPDATE trigger=trigger
        """
        database.execute_query(
            query,
            (
                trigger,
                response,
                emoji,
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
        guild_id: int,
        trigger: str,
        new_response: Optional[str] = None,
        new_emoji: Optional[str] = None,
        is_emoji: Optional[bool] = None,
        is_full_match: Optional[bool] = None,
        is_global: Optional[bool] = None,
    ) -> bool:
        query = """
        UPDATE custom_reactions
        SET response = COALESCE(?, response),
            emoji = COALESCE(?, emoji),
            is_emoji = COALESCE(?, is_emoji),
            is_full_match = COALESCE(?, is_full_match),
            is_global = COALESCE(?, is_global),
            updated_at = ?
        WHERE guild_id = ? AND trigger = ?
        """
        database.execute_query(
            query,
            (
                new_response,
                new_emoji,
                is_emoji,
                is_full_match,
                is_global,
                datetime.utcnow(),
                guild_id,
                trigger,
            ),
        )
        return True

    async def delete_custom_reaction(self, guild_id: int, trigger: str) -> bool:
        query = """
        DELETE FROM custom_reactions
        WHERE guild_id = ? AND trigger = ?
        """
        database.execute_query(query, (guild_id, trigger))
        return True

    async def count_custom_reactions(self, guild_id: int) -> int:
        query = """
        SELECT COUNT(*) FROM custom_reactions
        WHERE guild_id = ?
        """
        count = database.select_query_one(query, (guild_id,))
        return count if count else 0
    
    async def increment_reaction_usage(self, guild_id: int, trigger: str) -> bool:
        query = """
        UPDATE custom_reactions
        SET usage_count = usage_count + 1,
            updated_at = ?
        WHERE guild_id = ? AND trigger = ?
        """
        database.execute_query(
            query,
            (
                datetime.utcnow(),
                guild_id,
                trigger,
            ),
        )
        return True
