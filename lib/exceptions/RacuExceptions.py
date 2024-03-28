from discord.ext import commands
import discord


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


class UserHierarchy(discord.DiscordException):
    pass


class BotHierarchy(discord.DiscordException):
    pass
