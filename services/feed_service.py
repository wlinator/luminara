from typing import Any

from db.database import execute_query, select_query_dict, select_query_one


class FeedService:
    def __init__(self):
        pass

    def upsert_feed(
        self,
        guild_id: int,
        channel_id: int,
        announcement_message: str,
        feed_type: str,
        username: str,
    ) -> None:
        query: str = """
        INSERT INTO feeds (guild_id, channel_id, announcement_message, feed_type, username)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            guild_id = VALUES(guild_id),
            channel_id = VALUES(channel_id), 
            announcement_message = VALUES(announcement_message), 
            feed_type = VALUES(feed_type), 
            username = VALUES(username), 
            updated_at = CURRENT_TIMESTAMP
        """
        execute_query(query, (guild_id, channel_id, announcement_message, feed_type, username))

    def fetch_feed(self, feed_id: int) -> dict[str, Any] | None:
        query: str = """
        SELECT * FROM feeds
        WHERE id = %s
        """
        result = select_query_one(query, (feed_id,))
        return result or None

    def fetch_feeds_by_guild(self, guild_id: int) -> list[dict[str, Any]]:
        query: str = """
        SELECT * FROM feeds
        WHERE guild_id = %s
        """
        results: list[dict[str, Any]] = select_query_dict(query, (guild_id,))
        return results

    def delete_feed(self, feed_id: int) -> None:
        query: str = """
        DELETE FROM feeds
        WHERE id = %s
        """
        execute_query(query, (feed_id,))
