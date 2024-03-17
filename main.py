import os
import platform
import sys
import traceback

import discord
from discord.ext import commands, bridge
from dotenv import load_dotenv

from lib import embeds_old
from config import json_loader
from handlers.ReactionHandler import ReactionHandler
from handlers.XPHandler import XPHandler
from handlers import LoggingHandler
from services.GuildConfig import GuildConfig
from services.Help import RacuHelp

load_dotenv('.env')
instance = os.getenv("INSTANCE")


def get_prefix(bot, message):
    return GuildConfig.get_prefix(message.guild.id)


client = bridge.Bot(
    owner_id=os.getenv('OWNER_ID'),
    command_prefix=get_prefix,
    intents=discord.Intents.all(),
    status=discord.Status.online,
    help_command=RacuHelp()
)

logs = LoggingHandler.setup_logger()


@client.event
async def on_ready():
    logs.info(f"[INFO] Logged in as {client.user.name}")
    logs.info(f"[INFO] discord.py API version: {discord.__version__}")
    logs.info(f"[INFO] Python version: {platform.python_version()}")
    logs.info(f"[INFO] Running on: {platform.system()} {platform.release()} ({os.name})")
    logs.info("-------------------------------------------------------")

    """
    https://docs.pycord.dev/en/stable/api/events.html#discord.on_ready
    This function isn't guaranteed to only be called once.
    Event is called when RESUME request fails.
    """


@client.listen()
async def on_message(message):
    if message.author.bot or instance.lower() != "main":
        return

    try:
        xp_handler = XPHandler()
        await xp_handler.process_xp(message)

        reaction_handler = ReactionHandler(reactions)
        await reaction_handler.handle_message(message)

    except Exception as error:
        logs.error(f"[EventHandler] on_message (check debug log): {error}", exc_info=False)
        logs.debug(f"[EventHandler] on_message (w/ stacktrace): {error}", exc_info=True)


@client.event
async def on_member_join(member):
    config = GuildConfig(member.guild.id)

    if (not config.welcome_channel_id

            # comment next line if debugging greetings
            or instance.lower() != "main"
    ):
        return

    embed = embeds_old.welcome_message(member, config.welcome_message)

    try:
        await member.guild.get_channel(config.welcome_channel_id).send(embed=embed, content=member.mention)
    except Exception as e:
        logs.info(f"[GreetingHandler] Message not sent in '{member.guild.name}'. Channel ID may be invalid. {e}")


@client.event
async def on_command_completion(ctx) -> None:
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
        # logs.info(
        #     f"Executed {executed_command} command in {ctx.guild.name} (ID: {ctx.guild.id}) "
        #     f"by {ctx.author} (ID: {ctx.author.id})"
        # )
        logs.info(f"[CommandHandler] {ctx.author.name} successfully did \"/{executed_command}\". "
                  f"| guild: {ctx.guild.name} ")
    else:
        # logs.info(
        #     f"Executed {executed_command} command by {ctx.author} (ID: {ctx.author.id}) in DMs."
        # )
        logs.info(f"[CommandHandler] {ctx.author.name} successfully did \"/{executed_command}\". | direct message")


@client.event
async def on_command_error(ctx, error) -> None:
    if isinstance(error, commands.CommandOnCooldown):

        seconds = error.retry_after
        minutes = seconds // 60
        seconds %= 60
        cooldown = "{:02d}:{:02d}".format(int(minutes), int(seconds))

        await ctx.respond(
            f"⏳ | **{ctx.author.name}** you are on cooldown. "
            f"You can use this command again in **{cooldown}**.",
            ephemeral=True)

        logs.info(f"[CommandHandler] {ctx.author.name} tried to do a command on cooldown.")

    elif isinstance(error, commands.MissingPermissions):
        await ctx.respond(strings["error_missing_permissions"].format(ctx.author.name), ephemeral=True)
        logs.info(f"[CommandHandler] {ctx.author.name} has missing permissions to do a command: "
                  f"{ctx.command.qualified_name}")

    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.respond(strings["error_bot_missing_permissions"].format(ctx.author.name), ephemeral=True)
        logs.info(f"[CommandHandler] Racu is missing permissions: {ctx.command.qualified_name}")

    elif isinstance(error, discord.CheckFailure) or isinstance(error, commands.CheckFailure):
        logs.info(
            f"[CommandHandler] {ctx.author.name} tried to do \"/{ctx.command.qualified_name}\" "
            f"but a check returned False.")

    else:
        logs.error(f"[CommandHandler] on_application_command_error: {error}")
        traceback.print_tb(error.original.__traceback__)


@client.event
async def on_error(event: str, *args, **kwargs) -> None:
    logs.error(f"[EventHandler] on_error INFO: errors.event.{event} | '*args': {args} | '**kwargs': {kwargs}")
    logs.error(f"[EventHandler] on_error EXCEPTION: {sys.exc_info()}")


# load all json
strings = json_loader.load_strings()
economy_config = json_loader.load_economy_config()
reactions = json_loader.load_reactions()


def load_modules():
    modules_list = [
        "birthdays",
        "economy",
        "misc"
    ]
    loaded_modules = set()

    for module in modules_list:
        if module in loaded_modules:
            continue # module is already loaded

        try:
            client.load_extension(f"modules.{module}")
            loaded_modules.add(module)
            logs.info(f"[MODULE] {module.upper()} loaded.")

        except Exception as e:
            logs.error(f"[MODULE] Failed to load module {module.upper()}: {e}")


if __name__ == '__main__':
    """
    This code is only ran when main.py is the primary module,
    thus NOT when main is imported from a cog. (sys.modules)
    """

    logs.info("RACU IS BOOTING")
    logs.info("\n")

    load_modules()

    # empty line to separate modules from system info in logs
    logs.info("\n")

    client.run(os.getenv('TOKEN'))
