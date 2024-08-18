import discord
from discord.ext import bridge, commands
from discord.ext.commands import guild_only

from modules.moderation import ban, cases, kick, softban, timeout, warn


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @bridge.bridge_command(
        name="ban",
        aliases=["b"],
        description="Ban a user from the server.",
        help="Bans a user from the server, you can use ID or mention them.",
        contexts={discord.InteractionContextType.guild},
    )
    @bridge.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @guild_only()
    async def ban_command(
            self,
            ctx,
            target: discord.User,
            *,
            reason: str | None = None,
    ):
        await ban.ban_user(self, ctx, target, reason)

    @bridge.bridge_command(
        name="case",
        aliases=["c"],
        description="View a case by its number.",
        help="Views a case by its number in the server.",
        contexts={discord.InteractionContextType.guild},
    )
    @bridge.has_permissions(view_audit_log=True)
    @guild_only()
    async def case_command(self, ctx, case_number: int):
        await cases.view_case_by_number(ctx, ctx.guild.id, case_number)

    @bridge.bridge_command(
        name="cases",
        aliases=["caselist"],
        description="View all cases in the server.",
        help="Lists all moderation cases for the current server.",
        contexts={discord.InteractionContextType.guild},
    )
    @bridge.has_permissions(view_audit_log=True)
    @guild_only()
    async def cases_command(self, ctx):
        await cases.view_all_cases_in_guild(ctx, ctx.guild.id)

    @bridge.bridge_command(
        name="editcase",
        aliases=["uc", "ec"],
        description="Edit the reason for a case.",
        help="Updates the reason for a specific case in the server.",
        contexts={discord.InteractionContextType.guild},
    )
    @bridge.has_permissions(view_audit_log=True)
    @guild_only()
    async def edit_case_command(self, ctx, case_number: int, *, new_reason: str):
        await cases.edit_case_reason(ctx, ctx.guild.id, case_number, new_reason)

    @bridge.bridge_command(
        name="kick",
        aliases=["k"],
        description="Kick a user from the server.",
        help="Kicks a user from the server.",
        contexts={discord.InteractionContextType.guild},
    )
    @bridge.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @guild_only()
    async def kick_command(
            self,
            ctx,
            target: discord.Member,
            *,
            reason: str | None = None,
    ):
        await kick.kick_user(self, ctx, target, reason)

    @bridge.bridge_command(
        name="modcases",
        aliases=["moderatorcases", "mc"],
        description="View all cases by a specific moderator.",
        help="Lists all moderation cases handled by a specific moderator in the current server.",
        contexts={discord.InteractionContextType.guild},
    )
    @bridge.has_permissions(view_audit_log=True)
    @guild_only()
    async def moderator_cases_command(self, ctx, moderator: discord.Member):
        await cases.view_all_cases_by_mod(ctx, ctx.guild.id, moderator)

    @bridge.bridge_command(
        name="softban",
        aliases=["sb"],
        description="Softban a user from the server.",
        help="Softbans a user from the server (ban and immediately unban to delete messages).",
        contexts={discord.InteractionContextType.guild},
    )
    @bridge.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @guild_only()
    async def softban_command(
            self,
            ctx,
            target: discord.Member,
            *,
            reason: str | None = None,
    ):
        await softban.softban_user(ctx, target, reason)

    @bridge.bridge_command(
        name="timeout",
        aliases=["t", "to"],
        description="Timeout a user.",
        help="Timeouts a user in the server for a specified duration.",
        contexts={discord.InteractionContextType.guild},
    )
    @bridge.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @guild_only()
    async def timeout_command(
            self,
            ctx,
            target: discord.Member,
            duration: str,
            *,
            reason: str | None = None,
    ):
        await timeout.timeout_user(self, ctx, target, duration, reason)

    @bridge.bridge_command(
        name="unban",
        aliases=["ub", "pardon"],
        description="Unbans a user from the server.",
        help="Unbans a user from the server, you can use ID or provide their username.",
        contexts={discord.InteractionContextType.guild},
    )
    @bridge.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @guild_only()
    async def unban_command(
            self,
            ctx,
            target: discord.User,
            *,
            reason: str | None = None,
    ):
        await ban.unban_user(ctx, target, reason)

    @bridge.bridge_command(
        name="untimeout",
        aliases=["removetimeout", "rto", "uto"],
        description="Remove timeout from a user.",
        help="Removes the timeout from a user in the server.",
        contexts={discord.InteractionContextType.guild},
    )
    @bridge.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @guild_only()
    async def untimeout_command(
            self,
            ctx,
            target: discord.Member,
            *,
            reason: str | None = None,
    ):
        await timeout.untimeout_user(ctx, target, reason)

    @bridge.bridge_command(
        name="warn",
        aliases=["w"],
        description="Warn a user.",
        help="Warns a user in the server.",
        contexts={discord.InteractionContextType.guild},
    )
    @bridge.has_permissions(kick_members=True)
    @guild_only()
    async def warn_command(
            self,
            ctx,
            target: discord.Member,
            *,
            reason: str | None = None,
    ):
        await warn.warn_user(ctx, target, reason)


def setup(client):
    client.add_cog(Moderation(client))
