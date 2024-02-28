import logging

import discord
from discord.ext import commands

from main import strings

logs = logging.getLogger('Racu.Core')


def hierarchy_check(user, target):
    if target.top_role >= user.top_role:
        return False
    else:
        return True


class SimpleModCog(commands.Cog):
    def __init__(self, client):
        self.bot = client

    """
    This cog contains simple moderation commands
    Fallback? Use Discord's built-ins.
    """

    @commands.slash_command(
        name="kick",
        description="Kick a member.",
        guild_only=True
    )
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick_command(self, ctx, *, target: discord.Member):

        if not hierarchy_check(ctx.author, target):
            return await ctx.respond(content=strings["error_hierarchy"].format(ctx.author.name), ephemeral=True)

        dm_channel = False

        try:
            await ctx.guild.kick(user=target, reason=f"moderator: {ctx.author.name}")
            await ctx.respond(strings["mod_kick"].format(ctx.author.name, target.name))

            dm_channel = True
            await target.send(strings["mod_kick_dm"].format(target.name, ctx.guild.name))

        except Exception as err:
            if not dm_channel:
                await ctx.respond(strings["error_mod_invoke_error"].format(ctx.author.name), ephemeral=True)

            logs.error(f"[CommandHandler] error during kick command: {err}")

    @commands.slash_command(
        name="ban",
        description="Ban a member.",
        guild_only=True
    )
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban_command(self, ctx, *, target: discord.Member, delete_messages: discord.Option(bool)):

        if not hierarchy_check(ctx.author, target):
            return await ctx.respond(content=strings["error_hierarchy"].format(ctx.author.name), ephemeral=True)

        dm_channel = False
        seconds = 0

        if delete_messages:
            seconds = 604800

        try:
            await ctx.guild.ban(user=target, reason=f"moderator: {ctx.author.name}", delete_message_seconds=seconds)
            await ctx.respond(strings["mod_ban"].format(ctx.author.name, target.name))

            dm_channel = True
            await target.send(strings["mod_ban_dm"].format(target.name, ctx.guild.name))

        except Exception as err:
            if not dm_channel:
                await ctx.respond(strings["error_mod_invoke_error"].format(ctx.author.name), ephemeral=True)

            logs.error(f"[CommandHandler] error during ban command: {err}")


def setup(client):
    client.add_cog(SimpleModCog(client))
