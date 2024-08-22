import asyncio
import contextlib
import random
import time
from typing import Optional

import discord
from discord.ext import commands
from discord.ext.commands import TextChannelConverter

from Client import LumiBot
from lib import formatter
from lib.constants import CONST
from services.blacklist_service import BlacklistUserService
from services.config_service import GuildConfig
from services.xp_service import XpRewardService, XpService


class XPHandler:
    def __init__(self, client: LumiBot, message: discord.Message) -> None:
        """
        Initializes the XPHandler with the given client and message.

        Args:
            client (LumiBot): The bot client.
            message (discord.Message): The message object.
        """
        self.client = client
        self.message: discord.Message = message
        self.author: discord.Member | discord.User = message.author
        self.guild: discord.Guild | None = message.guild
        self.xp_conf: XpService = XpService(
            self.author.id,
            self.guild.id if self.guild else 0,
        )
        self.guild_conf: Optional[GuildConfig] = None

    def process(self) -> bool:
        """
        Processes the XP gain and level up for the user.

        Returns:
            bool: True if the user leveled up, False otherwise.
        """
        _xp: XpService = self.xp_conf
        _now: float = time.time()
        leveled_up: bool = False

        if _xp.cooldown_time and _now < _xp.cooldown_time:
            return False

        # Award the amount of XP specified in .env
        _xp.xp += _xp.xp_gain

        # Check if total XP now exceeds the XP required to level up
        if _xp.xp >= XpService.xp_needed_for_next_level(_xp.level):
            _xp.level += 1
            _xp.xp = 0
            leveled_up = True

        _xp.cooldown_time = _now + _xp.new_cooldown
        _xp.push()
        return leveled_up

    async def notify(self) -> None:
        """
        Notifies the user and the guild about the level up.
        """
        if self.guild is None:
            return

        _xp: XpService = self.xp_conf
        _gd: GuildConfig = GuildConfig(self.guild.id)

        level_message: Optional[str] = None  # Initialize level_message

        if isinstance(self.author, discord.Member):
            level_message = await self.get_level_message(_gd, _xp, self.author)

        if level_message:
            level_channel: Optional[discord.TextChannel] = await self.get_level_channel(
                self.message,
                _gd,
            )

            if level_channel:
                await level_channel.send(content=level_message)
            else:
                await self.message.reply(content=level_message)

    async def reward(self) -> None:
        """
        Rewards the user with a role for leveling up.
        """
        if self.guild is None:
            return

        _xp: XpService = self.xp_conf
        _rew: XpRewardService = XpRewardService(self.guild.id)

        if role_id := _rew.get_role(_xp.level):
            reason: str = "Automated Level Reward"

            if role := self.guild.get_role(role_id):
                with contextlib.suppress(
                    discord.Forbidden,
                    discord.NotFound,
                    discord.HTTPException,
                ):
                    if isinstance(self.author, discord.Member):
                        await self.author.add_roles(role, reason=reason)
            previous, replace = _rew.should_replace_previous_reward(_xp.level)

            if replace and isinstance(self.author, discord.Member):
                if role := self.guild.get_role(previous or role_id):
                    with contextlib.suppress(
                        discord.Forbidden,
                        discord.NotFound,
                        discord.HTTPException,
                    ):
                        await self.author.remove_roles(role, reason=reason)

    async def get_level_channel(
        self,
        message: discord.Message,
        guild_config: GuildConfig,
    ) -> Optional[discord.TextChannel]:
        """
        Retrieves the level up notification channel for the guild.

        Args:
            message (discord.Message): The message object.
            guild_config (GuildConfig): The guild configuration.

        Returns:
            Optional[discord.TextChannel]: The level up notification channel, or None if not found.
        """
        if guild_config.level_channel_id and message.guild:
            context = await self.client.get_context(message)

            with contextlib.suppress(commands.BadArgument, commands.CommandError):
                return await TextChannelConverter().convert(
                    context,
                    str(guild_config.level_channel_id),
                )
        return None

    @staticmethod
    async def get_level_message(
        guild_config: GuildConfig,
        level_config: XpService,
        author: discord.Member,
    ) -> Optional[str]:
        """
        Retrieves the level up message for the user.

        Args:
            guild_config (GuildConfig): The guild configuration.
            level_config (XpService): The XP service configuration.
            author (discord.Member): The user who leveled up.

        Returns:
            Optional[str]: The level up message, or None if not found.
        """
        match guild_config.level_message_type:
            case 0:
                level_message = None
            case 1:
                level_message = XPHandler.messages_whimsical(level_config.level, author)
            case 2:
                if not guild_config.level_message:
                    level_message = XPHandler.level_message_generic(
                        level_config.level,
                        author,
                    )
                else:
                    level_message = formatter.template(
                        guild_config.level_message,
                        author.name,
                        level_config.level,
                    )
            case _:
                raise ValueError("Invalid level message type")

        return level_message

    @staticmethod
    def level_message_generic(level: int, author: discord.Member) -> str:
        """
        Generates a generic level up message.

        Args:
            level (int): The new level of the user.
            author (discord.Member): The user who leveled up.

        Returns:
            str: The generic level up message.
        """
        return CONST.STRINGS["level_up"].format(author.name, level)

    @staticmethod
    def messages_whimsical(level: int, author: discord.Member) -> str:
        """
        Generates a whimsical level up message.

        Args:
            level (int): The new level of the user.
            author (discord.Member): The user who leveled up.

        Returns:
            str: The whimsical level up message.
        """
        level_range: Optional[str] = None
        for key in CONST.LEVEL_MESSAGES.keys():
            start, end = map(int, key.split("-"))
            if start <= level <= end:
                level_range = key
                break

        if level_range is None:
            # Generic fallback
            return XPHandler.level_message_generic(level, author)

        message_list = CONST.LEVEL_MESSAGES[level_range]
        random_message = random.choice(message_list)
        start_string = CONST.STRINGS["level_up_prefix"].format(author.name)
        return start_string + random_message.format(level)


class XpListener(commands.Cog):
    def __init__(self, client: LumiBot) -> None:
        """
        Initializes the XpListener with the given client.

        Args:
            client (LumiBot): The bot client.
        """
        self.client: LumiBot = client

    @commands.Cog.listener("on_message")
    async def xp_listener(self, message: discord.Message) -> None:
        """
        Listens for messages and processes XP gain and level up.

        Args:
            message (discord.Message): The message object.
        """
        if BlacklistUserService.is_user_blacklisted(message.author.id):
            return

        if message.author.bot or message.guild is None:
            return

        _xp: XPHandler = XPHandler(self.client, message)
        if _xp.process():
            await asyncio.gather(
                _xp.notify(),
                _xp.reward(),
            )


def setup(client: LumiBot) -> None:
    client.add_cog(XpListener(client))
