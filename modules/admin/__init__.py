from typing import Optional

import discord
from discord.ext import commands

from modules.admin import award, blacklist, sql, sync


class BotAdmin(commands.Cog, name="Bot Admin"):
    """
    This module is intended for commands that only bot owners can do.
    For server configuration with Lumi, see the "config" module.
    """

    def __init__(self, client):
        self.client = client

    @commands.command(name="award")
    @commands.is_owner()
    async def award_command(self, ctx, user: discord.User, *, amount: int):
        return await award.cmd(ctx, user, amount)

    @commands.command(name="sqlselect", aliases=["sqls"])
    @commands.is_owner()
    async def select(self, ctx, *, query: str):
        return await sql.select_cmd(ctx, query)

    @commands.command(name="sqlinject", aliases=["sqli"])
    @commands.is_owner()
    async def inject(self, ctx, *, query: str):
        return await sql.inject_cmd(ctx, query)

    @commands.command(name="blacklist")
    @commands.is_owner()
    async def blacklist(self, ctx, user: discord.User, *, reason: Optional[str] = None):
        return await blacklist.blacklist_user(ctx, user, reason)

    @commands.command(name="sync")
    @commands.is_owner()
    async def sync_command(self, ctx):
        await sync.sync_commands(self.client, ctx)


def setup(client):
    client.add_cog(BotAdmin(client))
