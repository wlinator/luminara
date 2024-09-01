from io import BytesIO

import discord
import httpx
from discord import File
from discord.ext import commands


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
    client: httpx.AsyncClient = httpx.AsyncClient()
    response: httpx.Response = await client.get(url, timeout=10)
    response.raise_for_status()
    image_data: bytes = response.content
    image_file: BytesIO = BytesIO(image_data)
    image_file.seek(0)
    return File(image_file, filename="avatar.png")


class Avatar(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="avatar",
        aliases=["av"],
    )
    async def avatar(
        self,
        ctx: commands.Context[commands.Bot],
        member: discord.Member | None = None,
    ) -> None:
        """
        Get the avatar of a member.

        Parameters:
        -----------
        ctx : ApplicationContext
            The discord context object.
        member : Member
            The member to get the avatar of.
        """
        if member is None:
            member = await commands.MemberConverter().convert(ctx, str(ctx.author.id))

        guild_avatar: str | None = member.guild_avatar.url if member.guild_avatar else None
        profile_avatar: str | None = member.avatar.url if member.avatar else None

        files: list[File] = [await create_avatar_file(avatar) for avatar in [guild_avatar, profile_avatar] if avatar]

        if files:
            await ctx.send(files=files)
        else:
            await ctx.send(content="member has no avatar.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Avatar(bot))
