""" .ENV TEMPLATE
TOKEN=
OWNER_ID=
XP_GAIN=
COOLDOWN=
CASH_BALANCE_NAME=
SPECIAL_BALANCE_NAME=
"""

import logging
import os

import discord
from dotenv import load_dotenv

import db.tables
import sb_tools.resources
from config import json_loader
from data.Item import Item
from handlers.XPHandler import XPHandler

logging.basicConfig(level=logging.INFO)
load_dotenv('.env')

# load all json
strings = json_loader.load_strings()
economy_config = json_loader.load_economy_config()

sbbot = discord.Bot(
    owner_id=os.getenv('OWNER_ID'),
    intents=discord.Intents.all(),
    activity=discord.Game(f"v{sb_tools.resources.__version__}"),
    status=discord.Status.do_not_disturb
)


def load_cogs(reload=False):
    for filename in os.listdir('./modules'):
        if filename.endswith('.py'):
            if not reload:
                sbbot.load_extension(f'modules.{filename[:-3]}')
            else:
                sbbot.reload_extension(f'modules.{filename[:-3]}')
                print(f"Module '{filename}' ready.")


@sbbot.event
async def on_ready():
    # wait until the bot is ready
    # then sync the sqlite3 database
    db.tables.sync_database()
    Item.insert_items()

    # reload all cogs to sync db parameters
    load_cogs(reload=True)

    """
    https://docs.pycord.dev/en/stable/api/events.html#discord.on_ready
    This function isn't guaranteed to only be called once.
    Event is called when RESUME request fails.
    """


@sbbot.event
async def on_message(message):
    if message.author.bot:
        return

    xp_handler = XPHandler()
    await xp_handler.process_xp(message)


load_cogs()
sbbot.run(os.getenv('TOKEN'))
