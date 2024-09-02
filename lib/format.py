import inspect
import textwrap
from typing import Any

import discord
from discord.ext import commands
from pytimeparse import parse  # type: ignore

from lib import exceptions
from lib.const import CONST
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


def format_case_number(case_number: int) -> str:
    """
    Formats a case number as a string with leading zeros if necessary.

    Args:
        case_number (int): The case number to format.

    Returns:
        str: The formatted case number as a string.
            If the case number is less than 1000, it will be padded with leading zeros to three digits.
            If the case number is 1000 or greater, it will be returned as a regular string.

    Examples:
        >>> format_case_number(1)
        '001'
        >>> format_case_number(42)
        '042'
        >>> format_case_number(999)
        '999'
        >>> format_case_number(1000)
        '1000'
    """
    return f"{case_number:03d}" if case_number < 1000 else str(case_number)


def get_prefix(ctx: commands.Context[commands.Bot]) -> str:
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


def get_invoked_name(ctx: commands.Context[commands.Bot]) -> str | None:
    """
    Attempts to get the alias of the command used. If the user used a SlashCommand, return the command name.

    Args:
        ctx (discord.ext.commands.Context): The context of the command invocation.

    Returns:
        str: The alias or name of the invoked command.
    """
    try:
        return ctx.invoked_with

    except (discord.app_commands.CommandInvokeError, AttributeError):
        return ctx.command.name if ctx.command else None


def format_duration_to_seconds(duration: str) -> int:
    """
    Converts a duration string to seconds. If the input is just an integer, it returns that integer as seconds.
    """
    if duration.isdigit():
        return int(duration)

    try:
        parsed_duration: int = parse(duration)  # type: ignore
        return max(0, parsed_duration)

    except Exception as e:
        raise exceptions.LumiException(CONST.STRINGS["error_invalid_duration"].format(duration)) from e


def format_seconds_to_duration_string(seconds: int) -> str:
    """
    Formats a duration in seconds to a human-readable string.
    Returns seconds if shorter than a minute.
    """
    if seconds < 60:
        return f"{seconds}s"

    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60

    if days > 0:
        return f"{days}d{hours}h" if hours > 0 else f"{days}d"
    if hours > 0:
        return f"{hours}h{minutes}m" if minutes > 0 else f"{hours}h"

    return f"{minutes}m"


def generate_usage(
    command: commands.Command[Any, Any, Any],
    flag_converter: type[commands.FlagConverter] | None = None,
) -> str:
    """
    Generate a usage string for a command with flags.
    Credit to https://github.com/allthingslinux/tux (thanks kaizen ;p)

    Parameters
    ----------
    command : commands.Command
        The command for which to generate the usage string.
    flag_converter : type[commands.FlagConverter]
        The flag converter class for the command.

    Returns
    -------
    str
        The usage string for the command. Example: "ban [target] -[reason] -<silent>"
    """

    # Get the name of the command
    command_name = command.qualified_name

    # Start the usage string with the command name
    usage = f"{command_name}"

    # Get the parameters of the command (excluding the `ctx` and `flags` parameters)
    parameters: dict[str, commands.Parameter] = command.clean_params

    flag_prefix = getattr(flag_converter, "__commands_flag_prefix__", "-")
    flags: dict[str, commands.Flag] = flag_converter.get_flags() if flag_converter else {}

    # Add non-flag arguments to the usage string
    for param_name, param in parameters.items():
        # Ignore these parameters
        if param_name in ["ctx", "flags"]:
            continue
        # Determine if the parameter is required
        is_required = param.default == inspect.Parameter.empty
        # Add the parameter to the usage string with required or optional wrapping
        usage += f" <{param_name}>" if is_required else f" [{param_name}]"

    # Add flag arguments to the usage string
    for flag_name, flag_obj in flags.items():
        # Determine if the flag is required or optional
        if flag_obj.required:
            usage += f" {flag_prefix}<{flag_name}>"
        else:
            usage += f" {flag_prefix}[{flag_name}]"

    return usage
