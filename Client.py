import os
import platform

import discord
from discord.ext import bridge
from loguru import logger

from lib.constants import CONST


class LumiBot(bridge.Bot):
    async def on_ready(self):
        """
        Called when the bot is ready.

        Logs various information about the bot and the environment it is running on.
        Note: This function isn't guaranteed to only be called once. The event is called when a RESUME request fails.
        """
        logger.info(f"{CONST.TITLE} v{CONST.VERSION}")
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
