import discord
from discord.ext import commands, bridge

from modules.moderation import ban


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @bridge.bridge_command(
        name="ban",
        aliases=["b"],
        guild_only=True
    )
    @bridge.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban_command(self, ctx, target: discord.User, *, reason: str = None):
        """
        Bans a user from the guild, you can mention the user, use ID or provide their username.
        """
        await ban.ban_user(self, ctx, target, reason)

    @bridge.bridge_command(
        name="unban",
        aliases=["ub", "pardon"],
        guild_only=True
    )
    @bridge.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    async def unban_command(self, ctx, target: discord.User, *, reason: str = None):
        """
        Unbans a user from the guild. If the user wasn't banned, this command will still process.
        """
        await ban.unban_user(ctx, target, reason)

    # async def cog_command_error(self, ctx: ApplicationContext, error: Exception) -> None:
    #     await ctx.respond(embed=ModErrors.mod_error(ctx, str(error)))


def setup(client):
    client.add_cog(Moderation(client))
