from typing import Optional, Dict, Any, List

from db.database import execute_query, select_query_one, select_query_dict


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
    ) -> int:
        # Get the next case number for the guild
        query: str = """
        SELECT IFNULL(MAX(case_number), 0) + 1
        FROM cases
        WHERE guild_id = %s
        """
        case_number = select_query_one(query, (guild_id,))

        if case_number is None:
            raise ValueError("Failed to retrieve the next case number.")

        # Insert the new case
        query: str = """
        INSERT INTO cases (
            guild_id, case_number, target_id, moderator_id, action_type, reason, duration, expires_at, modlog_message_id
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        execute_query(
            query,
            (
                guild_id,
                case_number,
                target_id,
                moderator_id,
                action_type.upper(),
                reason,
                duration,
                expires_at,
                modlog_message_id,
            ),
        )

        return int(case_number)

    def close_case(self, guild_id, case_number):
        query = """
        UPDATE cases
        SET is_closed = TRUE, updated_at = CURRENT_TIMESTAMP
        WHERE guild_id = %s AND case_number = %s
        """
        execute_query(query, (guild_id, case_number))

    def edit_case_reason(
        self,
        guild_id: int,
        case_number: int,
        new_reason: Optional[str] = None,
    ) -> bool:
        query = """
        UPDATE cases
        SET reason = COALESCE(%s, reason),
            updated_at = CURRENT_TIMESTAMP
        WHERE guild_id = %s AND case_number = %s
        """
        execute_query(
            query,
            (
                new_reason,
                guild_id,
                case_number,
            ),
        )
        return True

    def edit_case(self, guild_id, case_number, changes: dict):
        set_clause = ", ".join([f"{key} = %s" for key in changes.keys()])
        query = f"""
        UPDATE cases
        SET {set_clause}, updated_at = CURRENT_TIMESTAMP
        WHERE guild_id = %s AND case_number = %s
        """
        execute_query(query, (*changes.values(), guild_id, case_number))

    def fetch_case_by_id(self, case_id: int) -> Optional[Dict[str, Any]]:
        query: str = """
        SELECT * FROM cases
        WHERE id = %s
        LIMIT 1
        """
        result: List[Dict[str, Any]] = select_query_dict(query, (case_id,))
        return result[0] if result else None

    def fetch_case_by_guild_and_number(
        self,
        guild_id: int,
        case_number: int,
    ) -> Optional[Dict[str, Any]]:
        query: str = """
        SELECT * FROM cases
        WHERE guild_id = %s AND case_number = %s
        ORDER BY case_number DESC
        LIMIT 1
        """
        result: List[Dict[str, Any]] = select_query_dict(query, (guild_id, case_number))
        return result[0] if result else None

    def fetch_cases_by_guild(self, guild_id: int) -> List[Dict[str, Any]]:
        query: str = """
        SELECT * FROM cases
        WHERE guild_id = %s
        ORDER BY case_number DESC
        """
        results: List[Dict[str, Any]] = select_query_dict(query, (guild_id,))
        return results

    def fetch_cases_by_target(
        self,
        guild_id: int,
        target_id: int,
    ) -> List[Dict[str, Any]]:
        query: str = """
        SELECT * FROM cases
        WHERE guild_id = %s AND target_id = %s
        ORDER BY case_number DESC
        """
        results: List[Dict[str, Any]] = select_query_dict(query, (guild_id, target_id))
        return results

    def fetch_cases_by_moderator(
        self,
        guild_id: int,
        moderator_id: int,
    ) -> List[Dict[str, Any]]:
        query: str = """
        SELECT * FROM cases
        WHERE guild_id = %s AND moderator_id = %s
        ORDER BY case_number DESC
        """
        results: List[Dict[str, Any]] = select_query_dict(
            query,
            (guild_id, moderator_id),
        )
        return results

    def fetch_cases_by_action_type(
        self,
        guild_id: int,
        action_type: str,
    ) -> List[Dict[str, Any]]:
        query: str = """
        SELECT * FROM cases
        WHERE guild_id = %s AND action_type = %s
        ORDER BY case_number DESC
        """
        results: List[Dict[str, Any]] = select_query_dict(
            query,
            (guild_id, action_type.upper()),
        )
        return results
