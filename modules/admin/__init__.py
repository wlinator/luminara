import logging

import discord
from discord.ext import commands, bridge
import datetime, time
from lib.embeds.info import MiscInfo
from modules.admin import award
from lib.embeds.error import EconErrors

from lib import checks
from main import strings

logs = logging.getLogger('Racu.Core')


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






def setup(client):
    client.add_cog(Admin(client))
