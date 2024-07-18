from db.database import execute_query, select_query, select_query_one
from typing import Optional


class CaseService:
    def __init__(self):
        pass

    def create_case(
        self,
        guild_id: int,
        target_id: int,
        moderator_id: int,
        action_type: str,
        reason: Optional[str] = None,
        duration: Optional[int] = None,
        expires_at: Optional[str] = None,
        modlog_message_id: Optional[int] = None,
    ) -> None:
        # Resolve action type id from action type name
        action_type_id_query: str = """
        SELECT id FROM action_types WHERE name = %s
        """
        action_type_id = select_query_one(action_type_id_query, (action_type.upper(),))

        query: str = """
        CALL insert_case(%s, %s, %s, %s, %s, %s, %s, %s)
        """
        execute_query(
            query,
            (
                guild_id,
                target_id,
                moderator_id,
                action_type_id,
                reason,
                duration,
                expires_at,
                modlog_message_id,
            ),
        )

    def close_case(self, case_id):
        query = """
        UPDATE cases
        SET is_closed = TRUE, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        """
        execute_query(query, (case_id,))

    def edit_case(self, case_id, changes: dict):
        set_clause = ", ".join([f"{key} = %s" for key in changes.keys()])
        query = f"""
        UPDATE cases
        SET {set_clause}, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        """
        execute_query(query, (*changes.values(), case_id))

    def fetch_case_by_id(self, case_id):
        query = """
        SELECT * FROM cases
        WHERE id = %s
        """
        result = select_query_one(query, (case_id,))
        return dict(result) if result else None

    def fetch_case_by_guild_and_number(self, guild_id, case_number):
        query = """
        SELECT * FROM cases
        WHERE guild_id = %s AND case_number = %s
        ORDER BY case_number DESC
        """
        result = select_query_one(query, (guild_id, case_number))
        return dict(result) if result else None

    def fetch_cases_by_guild(self, guild_id):
        query = """
        SELECT * FROM cases
        WHERE guild_id = %s
        ORDER BY case_number DESC
        """
        results = select_query(query, (guild_id,))
        return [dict(row) for row in results]

    def fetch_cases_by_target(self, guild_id, target_id):
        query = """
        SELECT * FROM cases
        WHERE guild_id = %s AND target_id = %s
        ORDER BY case_number DESC
        """
        results = select_query(query, (guild_id, target_id))
        return [dict(row) for row in results]

    def fetch_cases_by_moderator(self, guild_id, moderator_id):
        query = """
        SELECT * FROM cases
        WHERE guild_id = %s AND moderator_id = %s
        ORDER BY case_number DESC
        """
        results = select_query(query, (guild_id, moderator_id))
        return [dict(row) for row in results]

    def fetch_cases_by_action_type(self, guild_id, action_type_id):
        query = """
        SELECT * FROM cases
        WHERE guild_id = %s AND action_type_id = %s
        ORDER BY case_number DESC
        """
        results = select_query(query, (guild_id, action_type_id))
        return [dict(row) for row in results]
