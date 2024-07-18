import discord
from discord.ext import bridge, commands

from modules.moderation import ban, cases


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

    @bridge.bridge_command(
        name="case",
        aliases=["c"],
        description="View a case by its number.",
        help="Views a case by its number in the server.",
        guild_only=True,
    )
    @bridge.has_permissions(view_audit_log=True)
    @commands.guild_only()
    async def case_command(
        self,
        ctx,
        case_number: int,
    ):
        await cases.view_case_by_number(ctx, ctx.guild.id, case_number)


def setup(client):
    client.add_cog(Moderation(client))
