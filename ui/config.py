import discord

import lib.format
from lib.const import CONST


async def create_boost_embed(
    user_name: str,
    user_avatar_url: str,
    boost_count: int,
    template: str | None = None,
    image_url: str | None = None,
) -> discord.Embed:
    """
    Create a boost embed message.

    Parameters
    ----------
    user_name : str
        The name of the user who boosted the server.
    user_avatar_url : str
        The avatar URL of the user who boosted the server.
    boost_count : int
        The total number of boosts the server has.
    template : str | None, optional
        The template text for the boost message.
    image_url : str | None, optional
        The image URL for the boost message.

    Returns
    -------
    discord.Embed
        The boost embed message.
    """
    embed = discord.Embed(
        color=discord.Colour.pink(),
        title=CONST.STRINGS["boost_default_title"],
        description=CONST.STRINGS["boost_default_description"].format(user_name),
    )

    if template:
        embed.description = lib.format.template(template, user_name)

    embed.set_author(name=user_name, icon_url=user_avatar_url)
    embed.set_image(url=image_url or CONST.BOOST_ICON)
    embed.set_footer(
        text=CONST.STRINGS["config_boost_total_count"].format(boost_count),
        icon_url=CONST.EXCLAIM_ICON,
    )

    return embed


def create_greet_embed(
    user_name: str,
    user_avatar_url: str,
    guild_name: str,
    template: str | None = None,
) -> discord.Embed:
    embed: discord.Embed = discord.Embed(
        color=discord.Colour.dark_embed(),
        description=CONST.STRINGS["greet_default_description"].format(
            guild_name,
        ),
    )
    if template and embed.description is not None:
        embed.description += CONST.STRINGS["greet_template_description"].format(
            lib.format.template(template, user_name),
        )

    embed.set_thumbnail(url=user_avatar_url)

    return embed
