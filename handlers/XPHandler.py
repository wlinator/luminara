import logging
import random
import time
import discord

from config import json_loader
from services.Currency import Currency
from services.Xp import Xp
from services.GuildConfig import GuildConfig
from lib import formatter

logs = logging.getLogger('Racu.Core')
strings = json_loader.load_strings()
level_messages = json_loader.load_levels()


class XPHandler:
    def __init__(self):
        pass

    async def process_xp(self, message):

        level_config = Xp(message.author.id, message.guild.id)
        guild_config = GuildConfig(message.guild.id)
        current_time = time.time()

        if level_config.ctime and current_time < level_config.ctime:
            return  # cooldown

        # award ENV XP_GAIN_PER_MESSAGE
        level_config.xp += level_config.xp_gain

        # check if total XP now exceeds level req
        xp_needed_for_new_level = Xp.xp_needed_for_next_level(level_config.level)

        if level_config.xp >= xp_needed_for_new_level:
            level_config.level += 1
            level_config.xp = 0

            level_message = await self.get_level_message(guild_config, level_config, message.author)

            if level_message:

                level_channel = await self.get_level_channel(message, guild_config)

                if level_channel:
                    await level_channel.send(content=level_message)
                else:
                    await message.reply(content=level_message)

            logs.info(f"[XpHandler] {message.author.name} leveled up to lv {level_config.level}.")

        else:
            logs.info(f"[XpHandler] {message.author.name} gained {level_config.xp_gain} XP | "
                      f"lv {level_config.level} with {level_config.xp} XP.")

        level_config.ctime = current_time + level_config.new_cooldown
        level_config.push()

        # Legacy code for Rave Cave level roles
        # turn into a global system soon
        await self.legacy_assign_level_role(message.author, level_config.level)

    @staticmethod
    async def get_level_channel(message, guild_config):
        if guild_config.level_channel_id:
            try:
                return message.guild.get_channel(guild_config.level_channel_id)
            except discord.HTTPException:
                pass  # channel not found

        return None

    @staticmethod
    async def get_level_message(guild_config, level_config, author):
        match guild_config.level_message_type:
            case 0:
                level_message = None
            case 1:
                level_message = XPHandler.level_messages_whimsical(level_config.level, author)
            case 2:
                if not guild_config.level_message:
                    level_message = XPHandler.level_message_generic(level_config.level, author)
                else:
                    level_message = formatter.template(guild_config.level_message,author.name, level_config.level)
            case _:
                raise Exception

        return level_message

    @staticmethod
    def level_message_generic(level, author):
        return strings["level_up"].format(author.name, level)

    @staticmethod
    def level_messages_whimsical(level, author):
        """
        v2 of the level messages, randomized output from levels.en-US.JSON.
        :param level:
        :param author:
        :return:
        """

        level_range = None
        for key in level_messages.keys():
            start, end = map(int, key.split('-'))
            if start <= level <= end:
                level_range = key
                break

        if level_range is None:
            # generic fallback
            return XPHandler.level_message_generic(level, author)

        message_list = level_messages[level_range]
        random_message = random.choice(message_list)
        start_string = strings["level_up_prefix"].format(author.name)
        return start_string + random_message.format(level)

    @staticmethod
    async def legacy_assign_level_role(user, level):

        guild = user.guild

        if (
            guild.id != 719227135151046699 or
            not (level % 5 == 0 and 5 <= level <= 100)
        ):
            return

        level_roles = {
            "level_5": 1118491431036792922,
            "level_10": 1118491486259003403,
            "level_15": 1118491512536301570,
            "level_20": 1118491532111126578,
            "level_25": 1118491554005393458,
            "level_30": 1118491572770713710,
            "level_35": 1118491596820840492,
            "level_40": 1118491622045405287,
            "level_45": 1118491650721853500,
            "level_50": 1118491681004732466,
            "level_55": 1191681166848303135,
            "level_60": 1191681220145319956,
            "level_65": 1191681253322264587,
            "level_70": 1191681274180554792,
            "level_75": 1191681293277216859,
            "level_80": 1191681312269017180,
            "level_85": 1191681337560662086,
            "level_90": 1191681359995998209,
            "level_95": 1191681384113262683,
            "level_100": 1191681405445492778,
            # Add more level roles as needed
        }

        current_level_role = None
        new_level_role_id = level_roles.get(f"level_{level}")

        for role in user.roles:
            if role.id in level_roles.values() and role.id != new_level_role_id:
                current_level_role = role
                break

        new_level_role = guild.get_role(new_level_role_id)
        await user.add_roles(new_level_role)

        if current_level_role:
            await user.remove_roles(current_level_role)
