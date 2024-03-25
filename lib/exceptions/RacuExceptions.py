from discord.ext import commands


class NotAllowedInChannel(commands.CheckFailure):
    """
    Raised when checks.allowed_in_channel() fails
    """
    def __init__(self, commands_channel):
        self.command_channel = commands_channel


class BirthdaysDisabled(commands.CheckFailure):
    """
    Raised when the birthdays module is disabled in ctx.guild
    """
    pass
