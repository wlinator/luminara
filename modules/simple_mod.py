import logging

import discord
from discord.ext import commands

from main import strings

racu_logs = logging.getLogger('Racu.Core')


def hierarchy_check(user, target):
    if target.top_role >= user.top_role:
        return False
    else:
        return True


class SimpleModCog(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot

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

        try:
            await ctx.guild.kick(user=target, reason=f"moderator: {ctx.author.name}")
            await ctx.respond(strings["mod_kick"].format(ctx.author.name, target.name))

            try:
                await target.send(strings["mod_kick_dm"].format(target.name, ctx.guild.name))
            except Exception as err:
                racu_logs.info(f"error during kick command (DM): {err}")

        except Exception as err:
            await ctx.respond(strings["error_mod_invoke_error"].format(ctx.author.name), ephemeral=True)
            racu_logs.info(f"error during kick command: {err}")


def setup(sbbot):
    sbbot.add_cog(SimpleModCog(sbbot))
