import asyncio
import os
import platform
from typing import Any

import discord
from discord.ext import commands
from loguru import logger

from db.database import run_migrations
from lib.const import CONST
from lib.loader import CogLoader


class Luminara(commands.Bot):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.is_shutting_down: bool = False
        self.setup_task: asyncio.Task[None] = asyncio.create_task(self.setup())

    async def on_ready(self) -> None:
        logger.success(f"{CONST.TITLE} v{CONST.VERSION}")
        logger.success(f"Logged in with ID {self.user.id if self.user else 'Unknown'}")
        logger.success(f"discord.py API version: {discord.__version__}")
        logger.success(f"Python version: {platform.python_version()}")
        logger.success(f"Running on: {platform.system()} {platform.release()} ({os.name})")

        if self.owner_ids:
            for owner in self.owner_ids:
                logger.info(f"Added bot administrator: {owner}")

        if not self.setup_task.done():
            await self.setup_task

    async def setup(self) -> None:
        try:
            run_migrations()
        except Exception as e:
            logger.error(f"Failed to setup: {e}")
            await self.shutdown()

        await self.load_cogs()

    async def load_cogs(self) -> None:
        await CogLoader.setup(bot=self)

    @commands.Cog.listener()
    async def on_disconnect(self) -> None:
        logger.warning("Disconnected from Discord.")

    async def shutdown(self) -> None:
        if self.is_shutting_down:
            logger.info("Shutdown already in progress. Exiting.")
            return

        self.is_shutting_down = True
        logger.info("Shutting down...")

        await self.close()

        if tasks := [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]:
            logger.debug(f"Cancelling {len(tasks)} outstanding tasks.")

            for task in tasks:
                task.cancel()

            await asyncio.gather(*tasks, return_exceptions=True)
            logger.debug("All tasks cancelled.")

        logger.info("Shutdown complete.")
