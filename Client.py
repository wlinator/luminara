import os
import platform
from typing import Optional

import discord
from discord.ext import bridge, commands
from discord.ext.commands import EmojiConverter, TextChannelConverter
from loguru import logger

from lib import metadata


class LumiBot(bridge.Bot):
    async def on_ready(self):
        """
        Called when the bot is ready.

        Logs various information about the bot and the environment it is running on.
        Note: This function isn't guaranteed to only be called once. The event is called when a RESUME request fails.
        """
        logger.info(f"{metadata.__title__} v{metadata.__version__}")
        logger.info(f"Logged in with ID {self.user.id if self.user else 'Unknown'}")
        logger.info(f"discord.py API version: {discord.__version__}")
        logger.info(f"Python version: {platform.python_version()}")
        logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")

        if self.owner_ids:
            for owner_id in self.owner_ids:
                logger.info(f"Added bot admin: {owner_id}")

    async def process_commands(self, message: discord.Message):
        """
        Processes commands sent by users.

        Args:
            message (discord.Message): The message object containing the command.
        """
        if message.author.bot:
            return

        ctx = await self.get_context(message)

        if ctx.command:
            # await ctx.trigger_typing()
            await self.invoke(ctx)

    @staticmethod
    async def convert_to_user(
        ctx: commands.Context | bridge.Context,
        user_id: int,
    ) -> Optional[discord.User]:
        """
        Converts a user ID to a User object.

        Args:
            ctx (commands.Context): The context in which the command was invoked.
            user_id (int): The ID of the user to convert.

        Returns:
            Optional[discord.User]: The User object, or None if conversion fails.
        """
        try:
            if isinstance(ctx, bridge.BridgeApplicationContext):
                return  # TODO: Implement this
            else:
                return await commands.UserConverter().convert(ctx, str(user_id))
        except (
            discord.HTTPException,
            discord.NotFound,
            discord.Forbidden,
            commands.BadArgument,
        ):
            return None

    @staticmethod
    async def convert_to_emoji(
        ctx: commands.Context | bridge.Context,
        emoji: str,
    ) -> Optional[discord.Emoji]:
        """
        Converts a emoji to an Emoji object.
        """
        converter = EmojiConverter()

        try:
            if isinstance(ctx, bridge.BridgeApplicationContext):
                return  # TODO: Implement this
            else:
                return await converter.convert(ctx, emoji)
        except commands.EmojiNotFound:
            logger.warning(f"Emoji not found: {emoji}")
            return None
        except (
            discord.HTTPException,
            discord.NotFound,
            discord.Forbidden,
            commands.BadArgument,
        ):
            return None

    @staticmethod
    async def convert_to_text_channel(
        ctx: commands.Context | bridge.Context,
        channel_id: int,
    ) -> Optional[discord.TextChannel]:
        """
        Converts a channel ID to a TextChannel object.

        Args:
            ctx (commands.Context): The context in which the command was invoked.
            channel_id (int): The ID of the channel to convert.

        Returns:
            Optional[discord.TextChannel]: The TextChannel object, or None if conversion fails.
        """
        converter = TextChannelConverter()

        try:
            if isinstance(ctx, bridge.BridgeApplicationContext):
                return  # TODO: Implement this
            else:
                return await converter.convert(ctx, str(channel_id))
        except (
            discord.HTTPException,
            discord.NotFound,
            discord.Forbidden,
            commands.BadArgument,
        ):
            return None

    @staticmethod
    async def convert_to_member(
        ctx: commands.Context,
        user_id: int,
    ) -> Optional[discord.Member]:
        """
        Converts a user ID to a Member object.

        Args:
            ctx (commands.Context): The context in which the command was invoked.
            user_id (int): The ID of the user to convert.

        Returns:
            Optional[discord.Member]: The Member object, or None if conversion fails.
        """
        converter = commands.MemberConverter()

        try:
            member = await converter.convert(ctx, str(user_id))
        except (
            discord.HTTPException,
            discord.NotFound,
            discord.Forbidden,
            commands.BadArgument,
        ):
            return None

        return member

    @staticmethod
    async def get_or_fetch_channel(
        guild: discord.Guild,
        channel_id: int,
    ) -> Optional[discord.abc.GuildChannel]:
        """
        Retrieves a channel from the guild's cache or fetches it from the API if not found.

        Args:
            guild (discord.Guild): The guild object.
            channel_id (int): The ID of the channel to retrieve or fetch.

        Returns:
            Optional[discord.abc.GuildChannel]: The channel object, or None if not found or an error occurs.
        """
        channel = guild.get_channel(channel_id)

        if not channel:
            try:
                channel = await guild.fetch_channel(channel_id)
            except (discord.HTTPException, discord.NotFound, discord.Forbidden):
                return None

        return channel

    @staticmethod
    async def get_or_fetch_member(
        guild: discord.Guild,
        user_id: int,
    ) -> Optional[discord.Member]:
        """
        Retrieves a member from the guild's cache or fetches them from the API if not found.

        Args:
            guild (discord.Guild): The guild object.
            user_id (int): The ID of the member to retrieve or fetch.

        Returns:
            Optional[discord.Member]: The member object, or None if not found or an error occurs.
        """
        member = guild.get_member(user_id)

        if not member:
            try:
                member = await guild.fetch_member(user_id)
            except (discord.HTTPException, discord.NotFound, discord.Forbidden):
                return None

        return member
