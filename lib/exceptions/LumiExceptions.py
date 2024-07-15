import discord
from discord.ext import commands


class NotAllowedInChannel(commands.CheckFailure):
    """
    Raised when checks.allowed_in_channel() fails.
    """

    def __init__(self, commands_channel):
        self.command_channel = commands_channel


class BirthdaysDisabled(commands.CheckFailure):
    """
    Raised when the birthdays module is disabled in ctx.guild.
    """

    pass


class LumiException(commands.CommandError):
    """
    A generic exception to raise for quick error handling.
    """

    def __init__(self, message="An error occurred."):
        self.message = message
        super().__init__(message)


class UserHierarchy(discord.DiscordException):
    pass


class BotHierarchy(discord.DiscordException):
    pass
