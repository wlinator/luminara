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
from datetime import datetime

import discord
import pytz
from dotenv import load_dotenv

import db.tables
import sb_tools.resources
from config import json_loader
from data.Item import Item
from handlers.ReactionHandler import ReactionHandler
from handlers.XPHandler import XPHandler


class RacuFormatter(logging.Formatter):
    def converter(self, timestamp):
        tz = pytz.timezone('US/Eastern')
        converted_time = datetime.fromtimestamp(timestamp, tz)
        return converted_time

    def formatTime(self, record, datefmt=None):
        timestamp = self.converter(record.created)
        if datefmt:
            return timestamp.strftime(datefmt)
        else:
            return str(timestamp)


def setup_logger():
    # Initialize the logger
    logger = logging.getLogger('Racu.Core')
    if logger.handlers:
        # Handlers already exist, no need to add more
        return logger

    logger.setLevel(logging.DEBUG)

    # Create console handler and set level and formatter
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = RacuFormatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Create file handler and set level and formatter
    file_handler = logging.FileHandler('racu.log')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = RacuFormatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
                                   datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger


racu_logs = setup_logger()
load_dotenv('.env')

# load all json
strings = json_loader.load_strings()
economy_config = json_loader.load_economy_config()
reactions = json_loader.load_reactions()

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
                racu_logs.info(f"Module {filename} loaded.")


@sbbot.event
async def on_ready():
    # wait until the bot is ready
    # then sync the sqlite3 database
    db.tables.sync_database()
    Item.insert_items()

    # reload all cogs to sync db parameters
    load_cogs(reload=True)
    racu_logs.info("RACU IS BOOTED/READY")

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

    reaction_handler = ReactionHandler(reactions)
    await reaction_handler.handle_message(message)


@sbbot.event
async def on_member_join(member):
    welcome_channel_id = 721862236112420915
    rules_channel_id = 719665850373898290
    self_roles_channel_id = 719665892652220536
    introductions_channel_id = 973619250507972618

    guild = member.guild

    if guild.id != 719227135151046699:
        return

    rules_channel = guild.get_channel(rules_channel_id)
    self_roles_channel = guild.get_channel(self_roles_channel_id)
    introductions_channel = guild.get_channel(introductions_channel_id)

    embed = discord.Embed(
        color=discord.Color.embed_background(),
        description=f"_ _\n**Welcome** to **Kaiju's Rave Cave** ↓↓↓\n"
                    f"[rules]({rules_channel.jump_url}) - "
                    f"[self roles]({self_roles_channel.jump_url}) - "
                    f"[introductions]({introductions_channel.jump_url})\n_ _"
    )
    embed.set_thumbnail(url=member.avatar.url)

    await guild.get_channel(welcome_channel_id).send(embed=embed, content=member.mention)


load_cogs()
sbbot.run(os.getenv('TOKEN'))
