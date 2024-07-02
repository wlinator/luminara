from io import BytesIO

import discord
import httpx

client = httpx.AsyncClient()


async def get_avatar(ctx, member: discord.Member | None = None) -> None:
    """
    Get the avatar of a member.

    Parameters:
    -----------
    interaction : discord.Interaction
        The discord interaction object.
    member : discord.Member
        The member to get the avatar of.
    """
    if member is None:
        member = ctx.author

    guild_avatar = member.guild_avatar.url if member.guild_avatar else None
    profile_avatar = member.avatar.url if member.avatar else None

    files = [
        await create_avatar_file(avatar)
        for avatar in [guild_avatar, profile_avatar]
        if avatar
    ]

    if files:
        await ctx.respond(files=files)
    else:
        await ctx.respond(content="Member has no avatar.")


async def create_avatar_file(url: str) -> discord.File:
    """
    Create a discord file from an avatar url.

    Parameters:
    -----------
    url : str
        The url of the avatar.

    Returns:
    --------
    discord.File
        The discord file.
    """
    response = await client.get(url, timeout=10)
    response.raise_for_status()
    image_data = response.content
    image_file = BytesIO(image_data)
    image_file.seek(0)
    return discord.File(image_file, filename="avatar.png")
