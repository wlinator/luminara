from db.database import execute_query, select_query_one


class ModLogService:
    def __init__(self):
        pass

    def set_modlog_channel(self, guild_id: int, channel_id: int) -> None:
        query: str = """
        INSERT INTO mod_log (guild_id, channel_id, is_enabled)
        VALUES (%s, %s, TRUE)
        ON DUPLICATE KEY UPDATE channel_id = VALUES(channel_id), is_enabled = TRUE, updated_at = CURRENT_TIMESTAMP
        """
        execute_query(query, (guild_id, channel_id))

    def disable_modlog_channel(self, guild_id: int) -> None:
        query: str = """
        UPDATE mod_log
        SET is_enabled = FALSE, updated_at = CURRENT_TIMESTAMP
        WHERE guild_id = %s
        """
        execute_query(query, (guild_id,))

    def fetch_modlog_channel_id(self, guild_id: int) -> int | None:
        query: str = """
        SELECT channel_id FROM mod_log
        WHERE guild_id = %s AND is_enabled = TRUE
        """
        result = select_query_one(query, (guild_id,))
        return result or None
