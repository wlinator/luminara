from discord.ext import commands


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
