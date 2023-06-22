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


@sbbot.event
async def on_ready():
    # wait until the bot is ready
    # then sync the sqlite3 database
    db.tables.sync_database()

    """
    https://docs.pycord.dev/en/stable/api/events.html#discord.on_ready
    This function isn't guaranteed to only be called once.
    Event is called when RESUME request fails.
    """


for filename in os.listdir('./modules'):
    if filename.endswith('.py'):
        sbbot.load_extension(f'modules.{filename[:-3]}')

sbbot.run(os.getenv('TOKEN'))
