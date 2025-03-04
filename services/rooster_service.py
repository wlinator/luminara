from typing import Any

from db import database


class RoosterService:
    def __init__(self, user_id: int) -> None:
        self.user_id: int = user_id
        self.rooster: dict[str, Any] | None = self.get_rooster()

    def get_rooster(self) -> dict[str, Any] | None:
        """
        Get the user's rooster or None if they don't have one
        """
        query = """
        SELECT *
        FROM roosters
        WHERE user_id = %s
        """

        result = database.select_query_dict(query, (self.user_id,))
        return result[0] if result else None

    def has_rooster(self) -> bool:
        """
        Check if the user has a rooster
        """
        return self.rooster is not None

    def get_rooster_equipment(self) -> dict[str, Any] | None:
        """
        Get the rooster's equipment with item details
        """
        if not self.has_rooster():
            return None

        query = """
        SELECT re.*,
               head.name as head_name, head.rarity as head_rarity, 
               body.name as body_name, body.rarity as body_rarity,
               leg.name as leg_name, leg.rarity as leg_rarity,
               spur.name as spur_name, spur.rarity as spur_rarity,
               talisman.name as talisman_name, talisman.rarity as talisman_rarity
        FROM rooster_equipment re
        LEFT JOIN rooster_items head ON re.head_item_id = head.id
        LEFT JOIN rooster_items body ON re.body_item_id = body.id
        LEFT JOIN rooster_items leg ON re.leg_item_id = leg.id
        LEFT JOIN rooster_items spur ON re.spur_item_id = spur.id
        LEFT JOIN rooster_items talisman ON re.talisman_item_id = talisman.id
        WHERE re.rooster_id = %s
        """

        if self.rooster is None:
            return None

        result = database.select_query_dict(query, (self.rooster["id"],))
        return result[0] if result else None

    def get_user_items(self) -> list[dict[str, Any]]:
        """
        Get all items owned by the user
        """
        query = """
        SELECT uri.*, ri.name, ri.description, ri.item_type, ri.rarity
        FROM user_rooster_items uri
        JOIN rooster_items ri ON uri.item_id = ri.id
        WHERE uri.user_id = %s
        """

        return database.select_query_dict(query, (self.user_id,))

    def get_campaign_progress(self) -> list[dict[str, Any]]:
        """
        Get the user's campaign progress
        """
        query = """
        SELECT cp.*, c.name, c.description, c.difficulty
        FROM user_campaign_progress cp
        JOIN cockfight_campaign c ON cp.campaign_id = c.id
        WHERE cp.user_id = %s
        ORDER BY c.required_level ASC
        """

        return database.select_query_dict(query, (self.user_id,))

    def get_achievements(self) -> list[dict[str, Any]]:
        """
        Get the user's achievements
        """
        query = """
        SELECT ua.*, ca.name, ca.description, ca.requirement_type, ca.requirement_value
        FROM user_achievements ua
        JOIN cockfight_achievements ca ON ua.achievement_id = ca.id
        WHERE ua.user_id = %s
        ORDER BY ua.unlocked DESC, ua.progress DESC
        """

        return database.select_query_dict(query, (self.user_id,))

    def create_rooster(self, name: str) -> dict[str, Any] | None:
        """
        Create a new rooster for the user
        """
        query = """
        INSERT INTO roosters (user_id, name)
        VALUES (%s, %s)
        """

        database.execute_query(query, (self.user_id, name))

        # Create empty equipment slots
        query = """
        INSERT INTO rooster_equipment (rooster_id)
        VALUES ((SELECT id FROM roosters WHERE user_id = %s))
        """

        database.execute_query(query, (self.user_id,))

        # Refresh rooster data
        self.rooster = self.get_rooster()
        return self.rooster

    def train_rooster(self, training_type: str) -> dict[str, Any] | None:
        """
        Train the rooster in a specific attribute
        """
        if not self.has_rooster() or self.rooster is None:
            return None

        valid_types = ["strength", "agility", "endurance", "technique", "luck"]
        if training_type not in valid_types:
            msg = f"Invalid training type. Must be one of: {', '.join(valid_types)}"
            raise ValueError(msg)

        # Add training record
        query = """
        INSERT INTO rooster_training (rooster_id, training_type)
        VALUES (%s, %s)
        """

        database.execute_query(query, (self.rooster["id"], training_type))

        # Update rooster stats
        query = f"""
        UPDATE roosters
        SET {training_type} = {training_type} + 1
        WHERE id = %s
        """

        database.execute_query(query, (self.rooster["id"],))

        # Refresh rooster data
        self.rooster = self.get_rooster()
        return self.rooster

    @staticmethod
    def format_rarity(rarity: str) -> str:
        """
        Format rarity with emoji and color
        """
        rarity_formats = {
            "common": "⚪ Common",
            "uncommon": "🟢 Uncommon",
            "rare": "🔵 Rare",
            "epic": "🟣 Epic",
            "legendary": "🟠 Legendary",
        }
        return rarity_formats.get(rarity, rarity)

    @staticmethod
    def format_difficulty(difficulty: str) -> str:
        """
        Format difficulty with emoji
        """
        difficulty_formats = {
            "tutorial": "📚 Tutorial",
            "easy": "🟢 Easy",
            "medium": "🟡 Medium",
            "hard": "🟠 Hard",
            "expert": "🔴 Expert",
            "master": "⭐ Master",
        }
        return difficulty_formats.get(difficulty, difficulty)
