from discord.ext import commands
from loguru import logger
import asyncio
from loader import CogLoader


class Luminara(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_shutting_down: bool = False
        self.setup_task: asyncio.Task = asyncio.create_task(self.setup())
        self.strip_after_prefix = True
        self.case_insensitive = True

    async def setup(self) -> None:
        try:
            pass
        except Exception as e:
            logger.error(f"Failed to setup: {e}")
        await self.load_cogs()

    async def load_cogs(self) -> None:
        logger.info("Loading cogs...")
        await CogLoader.setup(bot=self)

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logger.success(f"Logged in as {self.user}.")

        if not self.setup_task.done():
            await self.setup_task

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

        if tasks := [
            task for task in asyncio.all_tasks() if task is not asyncio.current_task()
        ]:
            logger.debug(f"Cancelling {len(tasks)} outstanding tasks.")

            for task in tasks:
                task.cancel()

            await asyncio.gather(*tasks, return_exceptions=True)
            logger.debug("All tasks cancelled.")

        logger.info("Shutdown complete.")
