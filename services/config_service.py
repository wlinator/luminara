from db import database


class GuildConfig:
    def __init__(self, guild_id):
        self.guild_id = guild_id
        self.birthday_channel_id = None
        self.command_channel_id = None
        self.intro_channel_id = None
        self.welcome_channel_id = None
        self.welcome_message = None
        self.boost_channel_id = None
        self.boost_message = None
        self.boost_image_url = None
        self.level_channel_id = None
        self.level_message = None
        self.level_message_type = 1

        self.fetch_or_create_config()

    def fetch_or_create_config(self):
        """
        Gets a Guild Config from the database or inserts a new row if it doesn't exist yet.
        """
        query = """
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
    def _extracted_from_fetch_or_create_config_14(self, query):
        (
            birthday_channel_id,
            command_channel_id,
            intro_channel_id,
            welcome_channel_id,
            welcome_message,
            boost_channel_id,
            boost_message,
            boost_image_url,
            level_channel_id,
            level_message,
            level_message_type,
        ) = database.select_query(query, (self.guild_id,))[0]

        self.birthday_channel_id = birthday_channel_id
        self.command_channel_id = command_channel_id
        self.intro_channel_id = intro_channel_id
        self.welcome_channel_id = welcome_channel_id
        self.welcome_message = welcome_message
        self.boost_channel_id = boost_channel_id
        self.boost_message = boost_message
        self.boost_image_url = boost_image_url
        self.level_channel_id = level_channel_id
        self.level_message = level_message
        self.level_message_type = level_message_type

    def push(self):
        query = """
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
    def get_prefix(message):
        """
        Gets the prefix from a given guild.
        This function is done as static method to make the prefix fetch process faster.
        """
        query = """
                SELECT prefix
                FROM guild_config
                WHERE guild_id = %s
                """

        prefix = database.select_query_one(
            query,
            (message.guild.id if message.guild else None,),
        )

        return prefix or "."

    @staticmethod
    def set_prefix(guild_id, prefix):
        """
        Sets the prefix for a given guild.
        """
        query = """
                UPDATE guild_config
                SET prefix = %s
                WHERE guild_id = %s;
                """

        database.execute_query(query, (prefix, guild_id))
