import discord
from discord.ext import commands, bridge

from modules.admin import award, sql


class BotAdmin(commands.Cog):
    """
    This module is intended for commands that only bot owners can do.
    For server configuration with Racu, see the "config" module.
    """

    def __init__(self, client):
        self.client = client

    @bridge.bridge_command(
        name="award",
        description="This command can only be performed by a bot administrator.",
        help="Awards cash to a specific user. This command can only be performed by a bot administrator.",
        guild_only=True
    )
    @commands.guild_only()
    @commands.is_owner()
    async def award_command(self, ctx, user: discord.User, *, amount: int):
        return await award.cmd(ctx, user, amount)

    @bridge.bridge_command(
        name="sqlselect",
        aliases=["sqls"],
        description="This command can only be performed by a bot administrator.",
        help="Perform a SELECT query in the database. This command can only be performed by a bot administrator."
    )
    @commands.is_owner()
    async def select(self, ctx, *, query: str):
        return await sql.select_cmd(ctx, query)

    @bridge.bridge_command(
        name="sqlinject",
        aliases=["sqli"],
        description="This command can only be performed by a bot administrator.",
        help="Change a value in the database. This command can only be performed by a bot administrator."
    )
    @commands.is_owner()
    async def inject(self, ctx, *, query: str):
        return await sql.inject_cmd(ctx, query)


def setup(client):
    client.add_cog(BotAdmin(client))
