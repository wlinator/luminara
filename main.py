import os

import discord
from dotenv import load_dotenv

import services.Client
import services.GuildConfig
import services.Help
import services.logging_service

load_dotenv('.env')
_logs = services.logging_service.setup_logger()


async def get_prefix(bot, message):
    try:
        return services.GuildConfig.GuildConfig.get_prefix(message.guild.id)
    except AttributeError:
        return "."


client = services.Client.RacuBot(
    owner_id=int(os.getenv('OWNER_ID')),
    command_prefix=get_prefix,
    intents=discord.Intents.all(),
    status=discord.Status.online,
    help_command=services.Help.RacuHelp()
)


def load_modules():
    loaded = set()

    # Load event listeners (handlers) and command cogs (modules)
    for directory in ["handlers", "modules"]:
        directory_path = os.path.join(os.getcwd(), directory)
        if not os.path.isdir(directory_path):
            continue

        items = [d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))] \
            if directory == "modules" else [f[:-3] for f in os.listdir(directory_path) if f.endswith('.py')]

        for item in items:
            if item in loaded:
                continue

            try:
                client.load_extension(f"{directory}.{item}")
                loaded.add(item)
                _logs.info(f'[{directory.upper()}] {item.upper()} loaded.')

            except Exception as e:
                _logs.error(f'[{directory.upper()}] Failed to load {item.upper()}: {e}')


if __name__ == '__main__':
    """
    This code is only ran when main.py is the primary module,
    thus NOT when main is imported from a cog. (sys.modules)
    """

    _logs.info("RACU IS BOOTING")
    _logs.info("\n")

    load_modules()

    # empty line to separate modules from system info in logs
    _logs.info("\n")

    client.run(os.getenv('TOKEN'))
