import os
import platform
import sys
import time

import discord
from discord.ext import commands
from dotenv import load_dotenv

import utils.resources
from config import json_loader
from handlers.ReactionHandler import ReactionHandler
from handlers.XPHandler import XPHandler
from handlers import LoggingHandler

load_dotenv('.env')
instance = os.getenv("INSTANCE")

client = discord.Bot(
    owner_id=os.getenv('OWNER_ID'),
    intents=discord.Intents.all(),
    activity=discord.Activity(
        name="Kaiju's Rave Cave",
        type=discord.ActivityType.listening,
    ),
    status=discord.Status.online
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


@client.event
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


@client.event
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

        logs.info(f"[CommandHandler] {ctx.author.name} tried to do a command on cooldown.")

    elif isinstance(error, commands.MissingPermissions):
        await ctx.respond(strings["error_missing_permissions"].format(ctx.author.name), ephemeral=True)
        logs.info(f"[CommandHandler] {ctx.author.name} has missing permissions to do a command: "
                       f"{ctx.command.qualified_name}")

    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.respond(strings["error_bot_missing_permissions"].format(ctx.author.name), ephemeral=True)
        logs.info(f"[CommandHandler] Racu is missing permissions: {ctx.command.qualified_name}")

    else:
        logs.error(f"[CommandHandler] on_application_command_error: {error}", exc_info=True)

        # if you use this, set "exc_info" to False above
        # logs.debug(f"[CommandHandler] on_application_command_error (w/ stacktrace): {error}", exc_info=True)


@client.event
async def on_error(event: str, *args, **kwargs) -> None:
    logs.error(f"[EventHandler] on_error INFO: errors.event.{event} | '*args': {args} | '**kwargs': {kwargs}")
    logs.error(f"[EventHandler] on_error EXCEPTION: {sys.exc_info()}")


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
                client.load_extension(module_name)
                loaded_modules.add(filename)
                logs.info(f"[MODULE] {filename[:-3].upper()} loaded.")

            except Exception as e:
                logs.error(f"[MODULE] Failed to load module {filename}: {e}")


if __name__ == '__main__':
    """
    This code is only ran when main.py is the primary module,
    thus NOT when main is imported from a cog. (sys.modules)
    """

    logs.info("RACU IS BOOTING")
    logs.info("\n")

    load_cogs()

    # empty line to separate modules from system info in logs
    logs.info("\n")

    client.run(os.getenv('TOKEN'))
