import logging
import os
import platform
import re
import sys
import time
from datetime import datetime

import discord
import pytz
from discord.ext import commands
from dotenv import load_dotenv

import sb_tools.resources
from config import json_loader
from data.Item import Item
from handlers.ReactionHandler import ReactionHandler
from handlers.XPHandler import XPHandler

load_dotenv('.env')
instance = os.getenv("INSTANCE")

sbbot = discord.Bot(
    owner_id=os.getenv('OWNER_ID'),
    intents=discord.Intents.all(),
    activity=discord.Activity(
        name="Kaiju's Rave Cave",
        type=discord.ActivityType.listening,
        state=f"v{sb_tools.resources.__version__}",
        timestamps={
            "start": time.time()
        },
        details="/daily | /level | /leaderboard",
        assets={
            "large_image": "ravecoin",
            "large_text": "Coins art by geardiabolus",
            "small_image": "admin_badge",
            "small_text": f"Made by {sb_tools.resources.__author__}",
        }
    ),
    status=discord.Status.online
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

    # Initialize the logger
    logger = logging.getLogger('Racu.Core')

    if logger.handlers:
        # Handlers already exist, no need to add more
        return logger

    logger.setLevel(logging.DEBUG)

    # Create console handler and set level and formatter
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = RacuFormatter('[%(asctime)s] [%(name)s] %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    logger.propagate = False
    logging.captureWarnings(True)

    return logger


racu_logs = setup_logger()


@sbbot.event
async def on_ready():
    racu_logs.info(f"[INFO] Logged in as {sbbot.user.name}")
    racu_logs.info(f"[INFO] discord.py API version: {discord.__version__}")
    racu_logs.info(f"[INFO] Python version: {platform.python_version()}")
    racu_logs.info(f"[INFO] Running on: {platform.system()} {platform.release()} ({os.name})")
    racu_logs.info("-------------------------------------------------------")

    """
    https://docs.pycord.dev/en/stable/api/events.html#discord.on_ready
    This function isn't guaranteed to only be called once.
    Event is called when RESUME request fails.
    """


@sbbot.event
async def on_message(message):
    if message.author.bot:
        return

    # remove if debugging leveling or reaction handler:
    # if instance.lower() != "main":
    #     return

    try:
        xp_handler = XPHandler()
        await xp_handler.process_xp(message)

        reaction_handler = ReactionHandler(reactions)
        await reaction_handler.handle_message(message)

    except Exception as error:
        racu_logs.error(f"[EventHandler] on_message (check debug log): {error}", exc_info=False)
        racu_logs.debug(f"[EventHandler] on_message (w/ stacktrace): {error}", exc_info=True)


@sbbot.event
async def on_member_join(member):
    guild = member.guild

    if guild.id != 719227135151046699:
        return

    # remove if debugging welcome messages:
    if instance.lower() != "main":
        return

    welcome_channel_id = 721862236112420915
    rules_channel_id = 719665850373898290
    introductions_channel_id = 973619250507972618

    rules_channel = guild.get_channel(rules_channel_id)
    introductions_channel = guild.get_channel(introductions_channel_id)

    embed = discord.Embed(
        color=discord.Color.embed_background(),
        description=f"_ _\n**Welcome** to **Kaiju's Rave Cave** ↓↓↓\n"
                    f"[rules]({rules_channel.jump_url}) - "
                    f"[introductions]({introductions_channel.jump_url})\n_ _"
    )

    embed.set_thumbnail(url=member.display_avatar)

    await guild.get_channel(welcome_channel_id).send(embed=embed, content=member.mention)


@sbbot.event
async def on_application_command_completion(ctx) -> None:
    """
    This code is executed when a slash_command has been successfully executed.
    This technically serves as a CommandHandler function
    :param ctx:
    :return:
    """
    full_command_name = ctx.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])

    if ctx.guild is not None:
        # racu_logs.info(
        #     f"Executed {executed_command} command in {ctx.guild.name} (ID: {ctx.guild.id}) "
        #     f"by {ctx.author} (ID: {ctx.author.id})"
        # )
        racu_logs.info(f"[CommandHandler] {ctx.author.name} successfully did \"/{executed_command}\". "
                       f"| guild: {ctx.guild.name} ")
    else:
        # racu_logs.info(
        #     f"Executed {executed_command} command by {ctx.author} (ID: {ctx.author.id}) in DMs."
        # )
        racu_logs.info(f"[CommandHandler] {ctx.author.name} successfully did \"/{executed_command}\". | direct message")


@sbbot.event
async def on_application_command_error(ctx, error) -> None:
    if isinstance(error, commands.CommandOnCooldown):

        seconds = error.retry_after
        minutes = seconds // 60
        seconds %= 60
        cooldown = "{:02d}:{:02d}".format(int(minutes), int(seconds))

        await ctx.respond(
            f"⏳ | **{ctx.author.name}** you are on cooldown. "
            f"You can use this command again in **{cooldown}**.",
            ephemeral=True)

        racu_logs.info(f"[CommandHandler] {ctx.author.name} tried to do a command on cooldown.")

    elif isinstance(error, commands.MissingPermissions):
        await ctx.respond(strings["error_missing_permissions"].format(ctx.author.name), ephemeral=True)
        racu_logs.info(f"[CommandHandler] {ctx.author.name} has missing permissions to do a command: "
                       f"{ctx.command.qualified_name}")

    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.respond(strings["error_bot_missing_permissions"].format(ctx.author.name), ephemeral=True)
        racu_logs.info(f"[CommandHandler] Racu is missing permissions: {ctx.command.qualified_name}")

    else:
        racu_logs.error(f"[CommandHandler] on_application_command_error: {error}", exc_info=True)

        # if you use this, set "exc_info" to False above
        # racu_logs.debug(f"[CommandHandler] on_application_command_error (w/ stacktrace): {error}", exc_info=True)


@sbbot.event
async def on_error(event: str, *args, **kwargs) -> None:
    racu_logs.error(f"[EventHandler] on_error INFO: errors.event.{event} | '*args': {args} | '**kwargs': {kwargs}")
    racu_logs.error(f"[EventHandler] on_error EXCEPTION: {sys.exc_info()}")


# load all json
strings = json_loader.load_strings()
economy_config = json_loader.load_economy_config()
reactions = json_loader.load_reactions()

# Keep track of loaded module filenames
loaded_modules = set()


def load_cogs():
    # sort modules alphabetically purely for an easier overview in logs
    for filename in sorted(os.listdir('./modules')):

        if filename in loaded_modules:
            continue  # module is already loaded

        if filename.endswith('.py'):
            module_name = f'modules.{filename[:-3]}'

            try:
                sbbot.load_extension(module_name)
                loaded_modules.add(filename)
                racu_logs.info(f"[MODULE] {filename[:-3].upper()} loaded.")

            except Exception as e:
                racu_logs.error(f"[MODULE] Failed to load module {filename}: {e}")


if __name__ == '__main__':
    """
    This code is only ran when main.py is the primary module,
    thus NOT when main is imported from a cog. (sys.modules)
    """

    racu_logs.info("RACU IS BOOTING")
    racu_logs.info("\n")

    load_cogs()

    # empty line to separate modules from system info in logs
    racu_logs.info("\n")

    # replace all items, if there are any changes they will be overwritten
    # Item.insert_items()

    sbbot.run(os.getenv('TOKEN'))
