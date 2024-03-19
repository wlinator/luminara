import discord


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


def get_prefix(ctx):
    """
    Attempt to get the prefix, if the command was used as a SlashCommand, return "/"
    """
    try:
        prefix = ctx.clean_prefix
    except (discord.ApplicationCommandInvokeError, AttributeError):
        prefix = "/"

    return prefix


def get_invoked_name(ctx):
    """
    Attempts to get the alias of the command used, if the user did a SlashCommand, return the name.
    """
    try:
        invoked_with = ctx.invoked_with
    except (discord.ApplicationCommandInvokeError, AttributeError):
        invoked_with = ctx.command.name

    return invoked_with
