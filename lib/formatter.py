import discord
import textwrap
from services.GuildConfig import GuildConfig


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
        "{level}": str(level) if level is not None else ""
    }

    for placeholder, value in replacements.items():
        text = text.replace(placeholder, value)

    return text


def shorten(text, width) -> str:
    return textwrap.shorten(text, width=width, placeholder="...")


def get_prefix(ctx):
    """
    Attempt to get the prefix.
    """
    try:
        return GuildConfig.get_prefix(ctx.guild.id)
    except AttributeError:
        return "."


def get_invoked_name(ctx):
    """
    Attempts to get the alias of the command used, if the user did a SlashCommand, return the name.
    """
    try:
        invoked_with = ctx.invoked_with
    except (discord.ApplicationCommandInvokeError, AttributeError):
        invoked_with = ctx.command.name

    return invoked_with
