import discord
from discord.ext import commands, bridge
from modules.admin import award, sql
from lib.embeds.error import EconErrors
from lib import checks


class Admin(commands.Cog):

    """
    This module is intended for commands that only bot owners can do.
    For server configuration with Racu, see the "config" module.
    """

    def __init__(self, client):
        self.client = client

    @bridge.bridge_command(
        name="award",
        description="Award currency - owner only command.",
        help="Awards cash to a specific user. This command can only be performed by a bot administrator.",
        guild_only=True
    )
    @commands.guild_only()
    @commands.check(checks.channel)
    @commands.check(checks.bot_owner)
    async def award_command(self, ctx, *, user: discord.User, amount: int):
        return await award.cmd(ctx, user, amount)

    @award_command.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.respond(embed=EconErrors.missing_bet(ctx))
        elif isinstance(error, commands.BadArgument):
            await ctx.respond(embed=EconErrors.bad_bet_argument(ctx))

    @bridge.bridge_command(
        name="sqlselect",
        aliases=["sqls"],
        description="Perform a SELECT query in the database.",
        help="Perform a SELECT query in the database. This can only be done by the owner of Racu."
    )
    @commands.check(checks.channel)
    @commands.check(checks.bot_owner)
    async def select(self, ctx, *, query: str):
        return await sql.select_cmd(ctx, query)

    @bridge.bridge_command(
        name="sqlinject",
        aliases=["sqli"],
        description="Change a value in the database. (DANGEROUS)",
        help="Change a value in the database. This can only be done by the owner of Racu. (DANGEROUS)"
    )
    @commands.check(checks.channel)
    @commands.check(checks.bot_owner)
    async def inject(self, ctx, *, query: str):
        return await sql.inject_cmd(ctx, query)


def setup(client):
    client.add_cog(Admin(client))
