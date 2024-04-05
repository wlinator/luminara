import logging
import random
import time
import asyncio

import discord

from config.parser import JsonCache
from discord.ext.commands import Cog
from lib import formatter
from services.GuildConfig import GuildConfig
from services.xp_service import XpService, XpRewardService

_strings = JsonCache.read_json("strings")
_messages = JsonCache.read_json("levels")
_logs = logging.getLogger('Racu.Core')


class XPHandler:
    def __init__(self, message):
        self.message = message
        self.author = message.author
        self.guild = message.guild
        self.channel = message.channel

        self.xp_conf = XpService(self.author.id, self.guild.id)
        self.guild_conf = None

    def process(self) -> bool:
        _xp = self.xp_conf
        _now = time.time()
        leveled_up = False

        if _xp.cooldown_time and _now < _xp.cooldown_time:
            return False

        # award the amount of XP specified in .env
        _xp.xp += _xp.xp_gain

        # check if total xp now exceeds the xp required to level up
        if _xp.xp >= XpService.xp_needed_for_next_level(_xp.level):
            _xp.level += 1
            _xp.xp = 0
            leveled_up = True

        _xp.cooldown_time = _now + _xp.new_cooldown
        _xp.push()
        return leveled_up

    async def notify(self) -> None:
        _xp = self.xp_conf
        _gd = GuildConfig(self.guild.id)

        level_message = await self.get_level_message(_gd, _xp, self.author)

        if level_message:
            level_channel = await self.get_level_channel(self.message, _gd)

            if level_channel:
                await level_channel.send(content=level_message)
            else:
                await self.message.reply(content=level_message)

    async def reward(self) -> None:
        _xp = self.xp_conf
        _rew = XpRewardService(self.guild.id)

        role_id = _rew.role(_xp.level)
        reason = 'Automated Level Reward'

        if role_id:

            role = self.guild.get_role(role_id)
            if role:
                try:
                    await self.author.add_roles(role, reason=reason)
                except (discord.Forbidden, discord.NotFound, discord.HTTPException):
                    pass

            previous = _rew.replace_previous_reward(_xp.level)
            if previous[1]:
                role = self.guild.get_role(previous[0])
                if role:
                    try:
                        await self.author.remove_roles(role, reason=reason)
                    except (discord.Forbidden, discord.NotFound, discord.HTTPException):
                        pass

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
                level_message = XPHandler.messages_whimsical(level_config.level, author)
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
        return _strings["level_up"].format(author.name, level)

    @staticmethod
    def messages_whimsical(level, author):
        """
        v2 of the level messages, randomized output from levels.en-US.JSON.
        :param level:
        :param author:
        :return:
        """

        level_range = None
        for key in _messages.keys():
            start, end = map(int, key.split('-'))
            if start <= level <= end:
                level_range = key
                break

        if level_range is None:
            # generic fallback
            return XPHandler.level_message_generic(level, author)

        message_list = _messages[level_range]
        random_message = random.choice(message_list)
        start_string = _strings["level_up_prefix"].format(author.name)
        return start_string + random_message.format(level)


class XpListener(Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener('on_message')
    async def xp_listener(self, message):
        if (
                message.author.bot or
                message.guild is None
        ):
            return

        _xp = XPHandler(message)
        leveled_up = _xp.process()

        if leveled_up:
            coros = [
                asyncio.create_task(_xp.notify()),
                asyncio.create_task(_xp.reward())
            ]
            await asyncio.wait(coros)


def setup(client):
    client.add_cog(XpListener(client))
