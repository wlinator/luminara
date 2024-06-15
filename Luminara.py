import os

import discord
import services.Client
import services.GuildConfig
import services.Help
import services.logging_service
import config.parser

_logs = services.logging_service.setup_logger()


async def get_prefix(bot, message):
    try:
        return services.GuildConfig.GuildConfig.get_prefix(message.guild.id)
    except AttributeError:
        return "."

client = services.Client.LumiBot(
    owner_id=int(os.environ.get('LUMI_OWNER_ID')),
    command_prefix=get_prefix,
    intents=discord.Intents.all(),
    status=discord.Status.online,
    help_command=services.Help.LumiHelp()
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
                _logs.info(f'[{directory.capitalize()}] {item.upper()} loaded.')

            except Exception as e:
                _logs.error(f'[{directory.capitalize()}] Failed to load {item.upper()}: {e}')


if __name__ == '__main__':
    """
    This code is only ran when Lumi.py is the primary module,
    so NOT when main is imported from a cog. (sys.modules)
    """

    _logs.info("LUMI IS BOOTING")
    _logs.info("\n")

    # cache all JSON
    [config.parser.JsonCache.read_json(file[:-5]) for file in os.listdir("config/JSON") if file.endswith(".json")]

    # load command and listener cogs
    load_modules()

    # empty line to separate modules from system info in logs
    _logs.info("\n")

    client.run(os.environ.get('LUMI_TOKEN'))
