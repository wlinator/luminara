import discord
from lib.exceptions import RacuExceptions


def actionable(target: discord.Member, invoker: discord.Member, bot_user: discord.Member) -> None:
    """
    Checks if the invoker and client have a higher role than the target user.

    Args:
        target: The member object of the target user.
        invoker: The member object of the user who invoked the command.
        bot_user: The discord.Bot.user object representing the bot itself.

    Returns:
        True if the client's highest role AND the invoker's highest role are higher than the target.
    """

    if target.top_role >= invoker.top_role and invoker != invoker.guild.owner:
        raise RacuExceptions.UserHierarchy

    elif target.top_role >= bot_user.top_role:
        raise RacuExceptions.BotHierarchy
