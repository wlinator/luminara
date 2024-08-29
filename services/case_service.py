from typing import Any

from db.database import execute_query, select_query_dict, select_query_one


class CaseService:
    def __init__(self) -> None:
        pass

    def create_case(
        self,
        guild_id: int,
        target_id: int,
        moderator_id: int,
        action_type: str,
        reason: str | None = None,
        duration: int | None = None,
        expires_at: str | None = None,
        modlog_message_id: int | None = None,
    ) -> int:
        # Get the next case number for the guild
        query: str = """
        SELECT IFNULL(MAX(case_number), 0) + 1
        FROM cases
        WHERE guild_id = %s
        """
        case_number: int | None = select_query_one(query, (guild_id,))

        if case_number is None:
            msg: str = "Failed to retrieve the next case number."
            raise ValueError(msg)

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

    def close_case(self, guild_id: int, case_number: int) -> None:
        query: str = """
        UPDATE cases
        SET is_closed = TRUE, updated_at = CURRENT_TIMESTAMP
        WHERE guild_id = %s AND case_number = %s
        """
        execute_query(query, (guild_id, case_number))

    def edit_case_reason(
        self,
        guild_id: int,
        case_number: int,
        new_reason: str | None = None,
    ) -> bool:
        query: str = """
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

    def edit_case(self, guild_id: int, case_number: int, changes: dict[str, Any]) -> None:
        set_clause: str = ", ".join([f"{key} = %s" for key in changes])
        query: str = f"""
        UPDATE cases
        SET {set_clause}, updated_at = CURRENT_TIMESTAMP
        WHERE guild_id = %s AND case_number = %s
        """
        execute_query(query, (*changes.values(), guild_id, case_number))

    def _fetch_cases(self, query: str, params: tuple[Any, ...]) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = select_query_dict(query, params)
        return results

    def _fetch_single_case(self, query: str, params: tuple[Any, ...]) -> dict[str, Any] | None:
        result = self._fetch_cases(query, params)
        return result[0] if result else None

    def fetch_case_by_id(self, case_id: int) -> dict[str, Any] | None:
        query: str = """
        SELECT * FROM cases
        WHERE id = %s
        LIMIT 1
        """
        return self._fetch_single_case(query, (case_id,))

    def fetch_case_by_guild_and_number(
        self,
        guild_id: int,
        case_number: int,
    ) -> dict[str, Any] | None:
        query: str = """
        SELECT * FROM cases
        WHERE guild_id = %s AND case_number = %s
        ORDER BY case_number DESC
        LIMIT 1
        """
        return self._fetch_single_case(query, (guild_id, case_number))

    def fetch_cases_by_guild(self, guild_id: int) -> list[dict[str, Any]]:
        query: str = """
        SELECT * FROM cases
        WHERE guild_id = %s
        ORDER BY case_number DESC
        """
        return self._fetch_cases(query, (guild_id,))

    def fetch_cases_by_target(
        self,
        guild_id: int,
        target_id: int,
    ) -> list[dict[str, Any]]:
        query: str = """
        SELECT * FROM cases
        WHERE guild_id = %s AND target_id = %s
        ORDER BY case_number DESC
        """
        return self._fetch_cases(query, (guild_id, target_id))

    def fetch_cases_by_moderator(
        self,
        guild_id: int,
        moderator_id: int,
    ) -> list[dict[str, Any]]:
        query: str = """
        SELECT * FROM cases
        WHERE guild_id = %s AND moderator_id = %s
        ORDER BY case_number DESC
        """
        return self._fetch_cases(query, (guild_id, moderator_id))

    def fetch_cases_by_action_type(
        self,
        guild_id: int,
        action_type: str,
    ) -> list[dict[str, Any]]:
        query: str = """
        SELECT * FROM cases
        WHERE guild_id = %s AND action_type = %s
        ORDER BY case_number DESC
        """
        return self._fetch_cases(query, (guild_id, action_type.upper()))
