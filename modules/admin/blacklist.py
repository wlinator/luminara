import discord
from services.blacklist_service import BlacklistUserService
from typing import Optional
from config.parser import JsonCache

resources = JsonCache.read_json("art")
exclaim_icon = resources["icons"]["exclaim"]
hammer_icon = resources["icons"]["hammer"]


async def blacklist_user(
    ctx, user: discord.User, reason: Optional[str] = None
) -> None:
    """
    Blacklists a user with an optional reason.

    Args:
        user_id (int): The ID of the user to blacklist.
        reason (str, optional): The reason for blacklisting the user. Defaults to "No reason was given".
    """
    blacklist_service = BlacklistUserService(user.id)
    blacklist_service.add_to_blacklist(reason)

    embed = discord.Embed(
        description=f"User `{user.name}` has been blacklisted from Luminara.",
        color=discord.Color.red(),
    )
    embed.set_author(name="User Blacklisted", icon_url=hammer_icon)
    embed.set_footer(text="There is no process to reinstate a blacklisted user. Appeals are not considered.", icon_url=exclaim_icon)
    
    await ctx.send(embed=embed)