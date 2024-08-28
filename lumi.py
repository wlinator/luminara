import sys
import asyncio
import discord
from discord.ext import commands
from loguru import logger
from lib.const import CONST
from client import Luminara

logger.remove()
logger.add(sys.stdout, format=CONST.LOG_FORMAT, colorize=True, level=CONST.LOG_LEVEL)


async def get_prefix(bot, message):
    return commands.when_mentioned_or(".")(bot, message)


async def main() -> None:
    if not CONST.TOKEN:
        logger.error("No token provided")
        return

    lumi: Luminara = Luminara(
        owner_ids=CONST.OWNER_IDS,
        intents=discord.Intents.all(),
        command_prefix=get_prefix,
        allowed_mentions=discord.AllowedMentions(everyone=False),
    )

    try:
        await lumi.start(CONST.TOKEN, reconnect=True)

    except KeyboardInterrupt:
        logger.info("Keyboard interrupt detected. Shutting down...")

    finally:
        logger.info("Closing resources...")
        await lumi.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
