import discord

footer_icon = "https://i.imgur.com/8xccUws.png"


def get_prefix(ctx):
    """
    Attempt to get the prefix, if the command was used as a SlashCommand, return "/"
    """
    try:
        prefix = ctx.clean_prefix
    except (discord.ApplicationCommandInvokeError, AttributeError):
        prefix = "/"

    return prefix


def MissingBet(ctx):
    """
    See MissingRequiredArgument
    """
    embed = discord.Embed(
        color=discord.Color.red(),
        description=f"**{ctx.author.name}** please enter a bet.",
    )
    embed.set_footer(text=f"For more info do '{get_prefix(ctx)}help {ctx.command}'",
                     icon_url=footer_icon)
    return embed


def BadBetArgument(ctx):
    """
    See BadArgument
    """
    embed = discord.Embed(
        color=discord.Color.red(),
        description=f"**{ctx.author.name}** the bet you entered is invalid.",
    )
    embed.set_footer(text=f"For more info do '{get_prefix(ctx)}help {ctx.command}'",
                     icon_url=footer_icon)
    return embed


def InsufficientBalance(ctx):
    """
    Error message for when the entered value exceeds the user's balance.
    """
    embed = discord.Embed(
        color=discord.Color.red(),
        description=f"**{ctx.author.name}** you don't have enough cash.",
    )
    embed.set_footer(text=f"Do '{get_prefix(ctx)}balance' to see how much you can spend.",
                     icon_url=footer_icon)
    return embed
