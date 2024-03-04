import datetime

import pytz

from db import database


class GuildConfig:
    def __init__(self, guild_id):
        self.guild_id = guild_id
        self.birthday_channel_id = None
        self.command_channel_id = None
        self.intro_channel_id = None
        self.welcome_channel_id = None
        self.level_channel_id = None
        self.level_message = None
        self.level_message_type = None

        self.fetch_or_create_config()

    
    def fetch_or_create_xp(self):
        """
        Gets a Guild Config from the database or inserts a new row if it doesn't exist yet.
        """
        query = """
                        SELECT birthday_channel_id, command_channel_id, intro_channel_id,
                                      welcome_channel_id, level_channel_id, level_message, level_message_type
                        FROM guild_config WHERE guild_id = %s
                        """

        try:
            (birthday_channel_id, command_channel_id, intro_channel_id, 
            welcome_channel_id, level_channel_id, level_message, level_message_type) = database.select_query(query, (self.guild_id,))[0]

        except (IndexError, TypeError):
            # No record found for the specified guild_id
            query =  "INSERT INTO guild_config (guild_id) VALUES (%s)"
            database.execute_query(query, (self.guild_id,))

            (birthday_channel_id, command_channel_id, intro_channel_id, 
            welcome_channel_id, level_channel_id, level_message, level_message_type) = (None, None, None, None, None, None, 1)

        self.birthday_channel_id = birthday_channel_id
        self.command_channel_id = command_channel_id
        self.intro_channel_id = intro_channel_id
        self.welcome_channel_id = welcome_channel_id
        self.level_channel_id = level_channel_id
        self.level_message = level_message
        self.level_message_type = level_message_type
    

    # INDIVIDUAL CHECKERS TO REDUCE RESOURCE COST
    @staticmethod
    def get_birthday_channel_id(guild_id):
        query =  """
                        SELECT birthday_channel_id
                        FROM guild_config
                        WHERE guild_id = %s;
                        """
        
        birthday_channel_id = database.select_query_one(query, (guild_id,))

        return birthday_channel_id

