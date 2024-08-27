import os
import sys

import discord
from discord.ext import commands
from loguru import logger

import Client
import services.config_service
import services.help_service
from db.database import run_migrations
from lib.constants import CONST
from lib.exceptions.LumiExceptions import Blacklisted
from services.blacklist_service import BlacklistUserService

# Remove the default logger configuration
logger.remove()

# Add a new logger configuration with colors and a short datetime format
log_format = (
    "<green>{time:YY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    # "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)
logger.add(sys.stdout, format=log_format, colorize=True, level="DEBUG")


async def get_prefix(bot, message):
    extras = services.config_service.GuildConfig.get_prefix(message)
    return commands.when_mentioned_or(*extras)(bot, message)


client = Client.LumiBot(
    owner_ids=CONST.OWNER_IDS,
    command_prefix=get_prefix,
    intents=discord.Intents.all(),
    status=discord.Status.online,
    help_command=services.help_service.LumiHelp(),
)


@client.check
async def blacklist_check(ctx):
    if BlacklistUserService.is_user_blacklisted(ctx.author.id):
        raise Blacklisted
    return True


def load_modules():
    loaded = set()

    # Load event listeners (handlers) and command cogs (modules)
    for directory in ["handlers", "modules"]:
        directory_path = os.path.join(os.getcwd(), directory)
        if not os.path.isdir(directory_path):
            continue

        items = (
            [
                d
                for d in os.listdir(directory_path)
                if os.path.isdir(os.path.join(directory_path, d))
            ]
            if directory == "modules"
            else [f[:-3] for f in os.listdir(directory_path) if f.endswith(".py")]
        )

        for item in items:
            if item in loaded:
                continue

            try:
                client.load_extension(f"{directory}.{item}")
                loaded.add(item)
                logger.debug(f"{item.upper()} loaded.")

            except Exception as e:
                logger.exception(f"Failed to load {item.upper()}: {e}")


if __name__ == "__main__":
    """
    This code is only ran when Lumi.py is the primary module,
    so NOT when main is imported from a cog. (sys.modules)
    """

    logger.info("LUMI IS BOOTING")

    # Run database migrations
    run_migrations()

    # load command and listener cogs
    load_modules()

    if not CONST.TOKEN:
        logger.error("token is not set in .env")
        exit(1)

    client.run(CONST.TOKEN)
