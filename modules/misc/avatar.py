from io import BytesIO
from typing import Optional

from discord import File, Member
from discord.ext import bridge
import httpx

client: httpx.AsyncClient = httpx.AsyncClient()


async def get_avatar(ctx: bridge.Context, member: Member) -> None:
    """
    Get the avatar of a member.

    Parameters:
    -----------
    ctx : ApplicationContext
        The discord context object.
    member : Member
        The member to get the avatar of.
    """    
    guild_avatar: Optional[str] = member.guild_avatar.url if member.guild_avatar else None
    profile_avatar: Optional[str] = member.avatar.url if member.avatar else None

    files: list[File] = [
        await create_avatar_file(avatar)
        for avatar in [guild_avatar, profile_avatar]
        if avatar
    ]

    if files:
        await ctx.respond(files=files)
    else:
        await ctx.respond(content="member has no avatar.")


async def create_avatar_file(url: str) -> File:
    """
    Create a discord file from an avatar url.

    Parameters:
    -----------
    url : str
        The url of the avatar.

    Returns:
    --------
    File
        The discord file.
    """
    response: httpx.Response = await client.get(url, timeout=10)
    response.raise_for_status()
    image_data: bytes = response.content
    image_file: BytesIO = BytesIO(image_data)
    image_file.seek(0)
    return File(image_file, filename="avatar.png")
