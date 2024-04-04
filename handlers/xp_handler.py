import logging
import random
import time

import discord

from config.parser import JsonCache
from lib import formatter
from services.GuildConfig import GuildConfig
from services.xp_service import XpService, XpRewardService

strings = JsonCache.read_json("strings")
level_messages = JsonCache.read_json("levels")
logs = logging.getLogger('Racu.Core')


class XPHandler:
    def __init__(self):
        pass

    async def process_xp(self, message):

        level_config = XpService(message.author.id, message.guild.id)
        guild_config = GuildConfig(message.guild.id)
        current_time = time.time()

        if level_config.ctime and current_time < level_config.ctime:
            return  # cooldown

        # award ENV XP_GAIN_PER_MESSAGE
        level_config.xp += level_config.xp_gain

        # check if total XP now exceeds level req
        xp_needed_for_new_level = XpService.xp_needed_for_next_level(level_config.level)

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

            await self.assign_level_role(message.guild, message.author, level_config.level)

            logs.info(f"[XpHandler] {message.author.name} leveled up to lv {level_config.level} "
                      f"in guild {message.guild.name} ({message.guild.id}).")

        else:
            logs.info(f"[XpHandler] {message.author.name} gained {level_config.xp_gain} XP | "
                      f"lv {level_config.level} with {level_config.xp} XP. | "
                      f"guild: {message.guild.name} ({message.guild.id})")

        level_config.ctime = current_time + level_config.new_cooldown
        level_config.push()

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
                    level_message = formatter.template(guild_config.level_message, author.name, level_config.level)
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
    async def assign_level_role(guild, user, level: int) -> None:
        _rew = XpRewardService(guild.id)
        role_id = _rew.role(level)
        reason = "Automated Level Reward"

        if role_id:

            role = guild.get_role(role_id)
            if role:
                try:
                    await user.add_roles(role, reason=reason)
                except (discord.Forbidden, discord.NotFound, discord.HTTPException):
                    pass

            previous = _rew.replace_previous_reward(level)
            if previous[1]:
                role = guild.get_role(previous[0])
                if role:
                    try:
                        await user.remove_roles(role, reason=reason)
                    except (discord.Forbidden, discord.NotFound, discord.HTTPException):
                        pass
