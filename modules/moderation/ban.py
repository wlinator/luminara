import logging

import discord

from lib import formatter
from lib.embeds.moderation import ModEmbeds, ModErrors
from modules.moderation import functions

_logs = logging.getLogger('Lumi.Core')


async def ban_user(cog, ctx, target: discord.User, reason):
    # see if user is in guild
    member = await cog.client.get_or_fetch_member(ctx.guild, target.id)

    if not reason:
        reason = "No reason provided."

    # member -> user is in the guild, check role hierarchy
    if member:
        bot_member = await cog.client.get_or_fetch_member(ctx.guild, ctx.bot.user.id)
        functions.actionable(member, ctx.author, bot_member)

        try:
            await member.send(embed=ModEmbeds.member_banned_dm(ctx, reason))
            dm_sent = True

        except (discord.HTTPException, discord.Forbidden):
            dm_sent = False

        # get user information, in case this can't be fetched after ban
        member_name = member.name
        member_id = member.id

        await member.ban(reason=f"moderator: {ctx.author.name} | reason: {formatter.shorten(reason, 200)}")
        return await ctx.respond(embed=ModEmbeds.member_banned(ctx, member_name, member_id, reason, dm_sent))

    # not a member in this guild, so ban right away
    else:
        await ctx.guild.ban(target, reason=f"moderator: {ctx.author.name} | reason: {formatter.shorten(reason, 200)}")
        return await ctx.respond(embed=ModEmbeds.user_banned(ctx, target.id, reason))


async def unban_user(ctx, target: discord.User, reason):
    if not reason:
        reason = "No reason provided."

    try:
        await ctx.guild.unban(target, reason=f"moderator: {ctx.author.name} | reason: {formatter.shorten(reason, 200)}")
        return await ctx.respond(embed=ModEmbeds.user_unban(ctx, target.id))

    except (discord.NotFound, discord.HTTPException):
        return await ctx.respond(embed=ModErrors.user_not_banned(ctx, target.id))
