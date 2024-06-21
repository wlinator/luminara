import os
import platform
from loguru import logger

import discord
from discord.ext import bridge

from lib import metadata


class LumiBot(bridge.Bot):
    async def on_ready(self):
        logger.info(f"{metadata.__title__} v{metadata.__version__}")
        logger.info(f"Logged in with ID {self.user.id}")
        logger.info(f"discord.py API version: {discord.__version__}")
        logger.info(f"Python version: {platform.python_version()}")
        logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")

        """
        https://docs.pycord.dev/en/stable/api/events.html#discord.on_ready
        This function isn't guaranteed to only be called once.
        Event is called when RESUME request fails.
        """

    async def process_commands(self, message: discord.Message):
        if message.author.bot:
            return

        ctx = await self.get_context(message)

        if ctx.command:
            await ctx.trigger_typing()
            await self.invoke(ctx)

    @staticmethod
    async def get_or_fetch_channel(guild, channel_id):
        channel = guild.get_channel(channel_id)

        if not channel:
            try:
                channel = await guild.fetch_channel(channel_id)

            except (discord.HTTPException, discord.NotFound, discord.Forbidden):
                return None

        return channel

    @staticmethod
    async def get_or_fetch_member(guild, user_id):
        member = guild.get_member(user_id)

        if not member:
            try:
                member = await guild.fetch_member(user_id)

            except (discord.HTTPException, discord.NotFound, discord.Forbidden):
                return None

        return member
