import textwrap

import discord

from database.controllers.guild_config import GuildConfigController


def template(text, username, level=None):
    """
    Replaces placeholders in the given text with actual values.

    Args:
        text (str): The template text containing placeholders.
        username (str): The username to replace "{user}" placeholder.
        level (int, optional): The level to replace "{level}" placeholder. Defaults to None.

    Returns:
        str: The formatted text.
    """
    replacements = {
        "{user}": username,
        "{level}": str(level) if level is not None else "",
    }

    for placeholder, value in replacements.items():
        text = text.replace(placeholder, value)

    return text


def shorten(text, width) -> str:
    return textwrap.shorten(text, width=width, placeholder="...")


async def get_prefix(ctx):
    """
    Attempt to get the prefix.
    """
    guild_config = GuildConfigController(ctx.guild.id)
    return await guild_config.get_prefix()


def get_invoked_name(ctx):
    """
    Attempts to get the alias of the command used, if the user did a SlashCommand, return the name.
    """
    try:
        invoked_with = ctx.invoked_with
    except (discord.ApplicationCommandInvokeError, AttributeError):
        invoked_with = ctx.command.name

    return invoked_with
