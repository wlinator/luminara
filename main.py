""" .ENV TEMPLATE
TOKEN=
INSTANCE=
OWNER_ID=
XP_GAIN=
COOLDOWN=
CASH_BALANCE_NAME=
SPECIAL_BALANCE_NAME=
DROPBOX_TOKEN=
"""

import logging
import os
import platform
import re
from datetime import datetime

import discord
import pytz
from discord.ext import commands
from dotenv import load_dotenv

import db.tables
import sb_tools.resources
from config import json_loader
from data.Item import Item
from handlers.ReactionHandler import ReactionHandler
from handlers.XPHandler import XPHandler

sbbot = discord.Bot(
    owner_id=os.getenv('OWNER_ID'),
    intents=discord.Intents.all(),
    activity=discord.Game(f"v{sb_tools.resources.__version__}"),
    status=discord.Status.do_not_disturb
)


class RacuFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None):
        super().__init__(fmt, datefmt)
        self.timezone = pytz.timezone('US/Eastern')

    def format(self, record):
        message = record.getMessage()
        message = re.sub(r'\n', '', message)  # Remove newlines
        message = re.sub(r'\s+', ' ', message)  # Remove multiple spaces
        message = message.strip()  # Remove leading and trailing spaces

        record.msg = message
        return super().format(record)

    def formatTime(self, record, datefmt=None):
        timestamp = self.timezone.localize(datetime.fromtimestamp(record.created))
        if datefmt:
            return timestamp.strftime(datefmt)
        else:
            return str(timestamp)


def setup_logger():
    # Create a "logs" subfolder if it doesn't exist
    logs_folder = 'logs'
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)

    # Generate the log file path for debug-level logs
    debug_log_file = os.path.join(logs_folder, 'debug.log')

    # Generate the log file path for info-level logs
    info_log_file = os.path.join(logs_folder, 'info.log')

    # Initialize the logger
    logger = logging.getLogger('Racu.Core')
    if logger.handlers:
        # Handlers already exist, no need to add more
        return logger

    logger.setLevel(logging.DEBUG)

    # Create console handler and set level and formatter
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = RacuFormatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Create debug file handler and set level and formatter
    debug_file_handler = logging.FileHandler(debug_log_file)
    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_formatter = RacuFormatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
                                         datefmt='%Y-%m-%d %H:%M:%S')
    debug_file_handler.setFormatter(debug_file_formatter)
    logger.addHandler(debug_file_handler)

    # Create info file handler and set level and formatter
    info_file_handler = logging.FileHandler(info_log_file)
    info_file_handler.setLevel(logging.INFO)
    info_file_formatter = RacuFormatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
                                        datefmt='%Y-%m-%d %H:%M:%S')
    info_file_handler.setFormatter(info_file_formatter)
    logger.addHandler(info_file_handler)

    logger.propagate = False
    logging.captureWarnings(True)

    return logger


racu_logs = setup_logger()


@sbbot.event
async def on_ready():
    racu_logs.info(f"Logged in as {sbbot.user.name}")
    racu_logs.info(f"discord.py API version: {discord.__version__}")
    racu_logs.info(f"Python version: {platform.python_version()}")
    racu_logs.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    racu_logs.info("-----------------------------------------")

    """
    https://docs.pycord.dev/en/stable/api/events.html#discord.on_ready
    This function isn't guaranteed to only be called once.
    Event is called when RESUME request fails.
    """


@sbbot.event
async def on_message(message):
    if message.author.bot:
        return

    try:
        xp_handler = XPHandler()
        await xp_handler.process_xp(message)

        reaction_handler = ReactionHandler(reactions)
        await reaction_handler.handle_message(message)

    except Exception as error:
        racu_logs.error(f"on_message (check debug log): {error}", exc_info=False)
        racu_logs.debug(f"on_message (w/ stacktrace): {error}", exc_info=True)


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


@sbbot.event
async def on_application_command_completion(ctx) -> None:
    """
    This code is executed when a slash_command has been successfully executed.
    :param ctx:
    :return:
    """
    full_command_name = ctx.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])

    if ctx.guild is not None:
        racu_logs.info(
            f"Executed {executed_command} command in {ctx.guild.name} (ID: {ctx.guild.id}) "
            f"by {ctx.author} (ID: {ctx.author.id})"
        )
    else:
        racu_logs.info(
            f"Executed {executed_command} command by {ctx.author} (ID: {ctx.author.id}) in DMs."
        )


@sbbot.event
async def on_application_command_error(ctx, error) -> None:
    if isinstance(error, commands.CommandOnCooldown):

        seconds = error.retry_after
        minutes = seconds // 60
        seconds %= 60
        cooldown = "{:02d}:{:02d}".format(int(minutes), int(seconds))

        await ctx.respond(
            f"⏳ | **{ctx.author.name}** you are on cooldown. "
            f"You can use this command again in **{cooldown}**.")

        racu_logs.info(f"commands.CommandOnCooldown | {ctx.author.name}")

    else:
        racu_logs.error(f"on_application_command_error (check debug log): {error}", exc_info=False)
        racu_logs.debug(f"on_application_command_error (w/ stacktrace): {error}", exc_info=True)


@sbbot.event
async def on_error(event: str, *args, **kwargs) -> None:
    racu_logs.error(f"on_error: errors.event.{event} | '*args': {args} | '**kwargs': {kwargs}")


# load all json
strings = json_loader.load_strings()
economy_config = json_loader.load_economy_config()
reactions = json_loader.load_reactions()

# Keep track of loaded module filenames
loaded_modules = set()


def load_cogs():
    for filename in os.listdir('./modules'):
        if filename.endswith('.py'):
            module_name = f'modules.{filename[:-3]}'

            # if module_name in sys.modules:
            #     continue  # Module is already loaded

            try:
                sbbot.load_extension(module_name)
                loaded_modules.add(filename)
                racu_logs.info(f"Module {filename} loaded.")

            except Exception as e:
                racu_logs.error(f"Failed to load module {filename}: {e}")


if __name__ == '__main__':
    """
    This code is only ran when main.py is the primary module,
    thus NOT when main is imported from a cog. (sys.modules)
    """

    racu_logs.info("RACU IS BOOTING")
    load_dotenv('.env')

    # load db
    db.tables.sync_database()
    Item.insert_items()

load_cogs()
sbbot.run(os.getenv('TOKEN'))
