import discord
from discord.ext import commands, bridge

from modules.moderation import ban


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @bridge.bridge_command(
        name="ban",
        aliases=["b"],
        description="Ban a user from the server.",
        help="Bans a user from the server, you can use ID or mention them.",
        guild_only=True,
    )
    @bridge.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban_command(
        self,
        ctx,
        target: discord.User,
        *,
        reason: str | None = None,
    ):
        await ban.ban_user(self, ctx, target, reason)

    @bridge.bridge_command(
        name="unban",
        aliases=["ub", "pardon"],
        description="Unbans a user from the server.",
        help="Unbans a user from the server, you can use ID or provide their username.",
        guild_only=True,
    )
    @bridge.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    async def unban_command(
        self,
        ctx,
        target: discord.User,
        *,
        reason: str | None = None,
    ):
        await ban.unban_user(ctx, target, reason)


def setup(client):
    client.add_cog(Moderation(client))
