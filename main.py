import asyncio
import os
import traceback

import discord
from dotenv import load_dotenv

from handlers import LoggingHandler, ErrorHandler
from handlers.ReactionHandler import ReactionHandler
from handlers.xp_handler import XPHandler
from lib.embeds.greet import Greet
from services.Client import RacuBot
from services.GuildConfig import GuildConfig
from services.Help import RacuHelp

load_dotenv('.env')
instance = os.getenv("INSTANCE")


def get_prefix(bot, message):
    try:
        return GuildConfig.get_prefix(message.guild.id)
    except AttributeError:
        return "."


client = RacuBot(
    owner_id=int(os.getenv('OWNER_ID')),
    command_prefix=get_prefix,
    intents=discord.Intents.all(),
    status=discord.Status.online,
    help_command=RacuHelp()
)

logs = LoggingHandler.setup_logger()


@client.listen()
async def on_message(message):
    if (
            message.author.bot or
            message.guild is None or
            instance.lower() != "main"
    ):
        return

    try:
        _xp = XPHandler(message)
        leveled_up = _xp.process()

        if leveled_up:
            coros = [
                asyncio.create_task(_xp.notify()),
                asyncio.create_task(_xp.reward())
            ]
            await asyncio.wait(coros)

        reaction_handler = ReactionHandler()
        await reaction_handler.handle_message(message)

    except Exception as error:
        logs.error(f"[EventHandler] on_message (check debug log): {error}", exc_info=True)
        traceback.print_tb(error.__traceback__)


@client.event
async def on_member_join(member):
    config = GuildConfig(member.guild.id)

    if (not config.welcome_channel_id

            # comment next line if debugging greetings
            or instance.lower() != "main"
    ):
        return

    embed = Greet.message(member, config.welcome_message)

    try:
        await member.guild.get_channel(config.welcome_channel_id).send(embed=embed, content=member.mention)
    except Exception as e:
        logs.info(f"[GreetingHandler] Message not sent in '{member.guild.name}'. Channel ID may be invalid. {e}")


@client.listen()
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


@client.listen()
async def on_command_error(ctx, error) -> None:
    await ErrorHandler.on_command_error(ctx, error)


@client.listen()
async def on_application_command_error(ctx, error) -> None:
    await ErrorHandler.on_command_error(ctx, error)


@client.event
async def on_error(event: str, *args, **kwargs) -> None:
    await ErrorHandler.on_error(event, *args, **kwargs)


def load_modules():
    module_list = [d for d in os.listdir("modules") if os.path.isdir(os.path.join("modules", d))]
    loaded_modules = set()

    for module in module_list:
        if module in loaded_modules:
            continue  # module is already loaded

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
