import asyncio
import sys

import discord
from discord.ext import commands
from loguru import logger

from lib.client import Luminara
from lib.const import CONST
from services.config_service import GuildConfig

logger.remove()
logger.add(sys.stdout, format=CONST.LOG_FORMAT, colorize=True, level=CONST.LOG_LEVEL)


async def get_prefix(bot: Luminara, message: discord.Message) -> list[str]:
    extras = GuildConfig.get_prefix(message)
    return commands.when_mentioned_or(*extras)(bot, message)


async def main() -> None:
    if not CONST.TOKEN:
        logger.error("No token provided")
        return

    lumi: Luminara = Luminara(
        owner_ids=CONST.OWNER_IDS,
        intents=discord.Intents.all(),
        command_prefix=get_prefix,
        allowed_mentions=discord.AllowedMentions(everyone=False),
        case_insensitive=True,
        strip_after_prefix=True,
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
