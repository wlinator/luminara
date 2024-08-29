from discord.ext import commands

from lib.const import CONST


class BirthdaysDisabled(commands.CheckFailure):
    """
    Raised when the birthdays module is disabled in ctx.guild.
    """


class LumiException(commands.CommandError):
    """
    A generic exception to raise for quick error handling.
    """

    def __init__(self, message: str = CONST.STRINGS["lumi_exception_generic"]):
        self.message = message
        super().__init__(message)


class Blacklisted(commands.CommandError):
    """
    Raised when a user is blacklisted.
    """

    def __init__(self, message: str = CONST.STRINGS["lumi_exception_blacklisted"]):
        self.message = message
        super().__init__(message)
