import textwrap

import discord
from discord.ext import commands

from services.config_service import GuildConfig


def template(text: str, username: str, level: int | None = None) -> str:
    """
    Replaces placeholders in the given text with actual values.

    Args:
        text (str): The template text containing placeholders.
        username (str): The username to replace the "{user}" placeholder.
        level (int | None, optional): The level to replace the "{level}" placeholder. Defaults to None.

    Returns:
        str: The formatted text with placeholders replaced by actual values.
    """
    replacements: dict[str, str] = {
        "{user}": username,
        "{level}": str(level) if level else "",
    }

    for placeholder, value in replacements.items():
        text = text.replace(placeholder, value)

    return text


def shorten(text: str, width: int = 200) -> str:
    """
    Shortens the input text to the specified width by adding a placeholder at the end if the text exceeds the width.

    Args:
        text (str): The text to be shortened.
        width (int): The maximum width of the shortened text (default is 200).

    Returns:
        str: The shortened text.

    Examples:
        shortened_text = shorten("Lorem ipsum dolor sit amet", 10)
    """
    return textwrap.shorten(text, width=width, placeholder="...")


def get_prefix(ctx: commands.Context) -> str:
    """
    Attempts to retrieve the prefix for the given guild context.

    Args:
        ctx (discord.ext.commands.Context): The context of the command invocation.

    Returns:
        str: The prefix for the guild. Defaults to "." if the guild or prefix is not found.
    """
    try:
        return GuildConfig.get_prefix(ctx.guild.id if ctx.guild else 0)
    except (AttributeError, TypeError):
        return "."


def get_invoked_name(ctx: commands.Context) -> str | None:
    """
    Attempts to get the alias of the command used. If the user used a SlashCommand, return the command name.

    Args:
        ctx (discord.ext.commands.Context): The context of the command invocation.

    Returns:
        str: The alias or name of the invoked command.
    """
    try:
        return ctx.invoked_with
    except (discord.ApplicationCommandInvokeError, AttributeError):
        return ctx.command.name if ctx.command else None
