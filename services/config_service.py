from typing import Any

from db import database


class GuildConfig:
    def __init__(self, guild_id: int) -> None:
        self.guild_id: int = guild_id
        self.birthday_channel_id: int | None = None
        self.command_channel_id: int | None = None
        self.intro_channel_id: int | None = None
        self.welcome_channel_id: int | None = None
        self.welcome_message: str | None = None
        self.boost_channel_id: int | None = None
        self.boost_message: str | None = None
        self.boost_image_url: str | None = None
        self.level_channel_id: int | None = None
        self.level_message: str | None = None
        self.level_message_type: int = 1

        self.fetch_or_create_config()

    def fetch_or_create_config(self) -> None:
        """
        Gets a Guild Config from the database or inserts a new row if it doesn't exist yet.
        """
        query: str = """
                        SELECT birthday_channel_id, command_channel_id, intro_channel_id,
                                      welcome_channel_id, welcome_message, boost_channel_id, 
                                      boost_message, boost_image_url, level_channel_id, 
                                      level_message, level_message_type
                        FROM guild_config WHERE guild_id = %s
                        """

        try:
            self._extracted_from_fetch_or_create_config_14(query)
        except (IndexError, TypeError):
            # No record found for the specified guild_id
            query = "INSERT INTO guild_config (guild_id) VALUES (%s)"
            database.execute_query(query, (self.guild_id,))

    # TODO Rename this here and in `fetch_or_create_config`
    def _extracted_from_fetch_or_create_config_14(self, query: str) -> None:
        result: tuple[Any, ...] = database.select_query(query, (self.guild_id,))[0]
        (
            self.birthday_channel_id,
            self.command_channel_id,
            self.intro_channel_id,
            self.welcome_channel_id,
            self.welcome_message,
            self.boost_channel_id,
            self.boost_message,
            self.boost_image_url,
            self.level_channel_id,
            self.level_message,
            self.level_message_type,
        ) = result

    def push(self) -> None:
        query: str = """
                UPDATE guild_config
                SET 
                    birthday_channel_id = %s,
                    command_channel_id = %s,
                    intro_channel_id = %s,
                    welcome_channel_id = %s,
                    welcome_message = %s,
                    boost_channel_id = %s,
                    boost_message = %s,
                    boost_image_url = %s,
                    level_channel_id = %s,
                    level_message = %s,
                    level_message_type = %s
                WHERE guild_id = %s;
                """

        database.execute_query(
            query,
            (
                self.birthday_channel_id,
                self.command_channel_id,
                self.intro_channel_id,
                self.welcome_channel_id,
                self.welcome_message,
                self.boost_channel_id,
                self.boost_message,
                self.boost_image_url,
                self.level_channel_id,
                self.level_message,
                self.level_message_type,
                self.guild_id,
            ),
        )

    @staticmethod
    def get_prefix(message: Any) -> str:
        """
        Gets the prefix from a given guild.
        This function is done as static method to make the prefix fetch process faster.
        """
        query: str = """
                SELECT prefix
                FROM guild_config
                WHERE guild_id = %s
                """

        prefix: str | None = database.select_query_one(
            query,
            (message.guild.id if message.guild else None,),
        )

        return prefix or "."

    @staticmethod
    def get_prefix_from_guild_id(guild_id: int) -> str:
        query: str = """
                SELECT prefix
                FROM guild_config
                WHERE guild_id = %s
                """

        return database.select_query_one(query, (guild_id,)) or "."

    @staticmethod
    def set_prefix(guild_id: int, prefix: str) -> None:
        """
        Sets the prefix for a given guild.
        """
        query: str = """
                UPDATE guild_config
                SET prefix = %s
                WHERE guild_id = %s;
                """

        database.execute_query(query, (prefix, guild_id))
