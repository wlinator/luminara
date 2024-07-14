import discord

from lib import formatter
from lib.constants import CONST
from lib.embed_builder import EmbedBuilder
from modules.moderation import functions


async def ban_user(cog, ctx, target: discord.User, reason):
    # see if user is in guild
    member = await cog.client.get_or_fetch_member(ctx.guild, target.id)

    if not reason:
        reason = CONST.STRINGS["mod_no_reason"]

    # member -> user is in the guild, check role hierarchy
    if member:
        bot_member = await cog.client.get_or_fetch_member(ctx.guild, ctx.bot.user.id)
        functions.actionable(member, ctx.author, bot_member)

        try:
            await member.send(
                embed=EmbedBuilder.create_warning_embed(
                    ctx,
                    author_text=CONST.STRINGS["mod_banned_author"],
                    description=CONST.STRINGS["mod_ban_dm"].format(
                        target.name, ctx.guild.name, reason
                    ),
                    show_name=False,
                )
            )
            dm_sent = True

        except (discord.HTTPException, discord.Forbidden):
            dm_sent = False

        await member.ban(
            reason=CONST.STRINGS["mod_reason"].format(
                ctx.author.name, formatter.shorten(reason, 200)
            )
        )
        return await ctx.respond(
            embed=EmbedBuilder.create_success_embed(
                ctx,
                author_text=CONST.STRINGS["mod_banned_author"],
                description=CONST.STRINGS["mod_banned_user"].format(target.id),
                footer_text=CONST.STRINGS["mod_dm_sent"]
                if dm_sent
                else CONST.STRINGS["mod_dm_not_sent"],
            )
        )

    # not a member in this guild, so ban right away
    else:
        await ctx.guild.ban(
            target,
            reason=CONST.STRINGS["mod_reason"].format(
                ctx.author.name, formatter.shorten(reason, 200)
            ),
        )
        return await ctx.respond(
            embed=EmbedBuilder.create_success_embed(
                ctx,
                author_text=CONST.STRINGS["mod_banned_author"],
                description=CONST.STRINGS["mod_banned_user"].format(target.id),
            )
        )


async def unban_user(ctx, target: discord.User, reason):
    if not reason:
        reason = CONST.STRINGS["mod_no_reason"]

    try:
        await ctx.guild.unban(
            target,
            reason=CONST.STRINGS["mod_reason"].format(
                ctx.author.name, formatter.shorten(reason, 200)
            ),
        )
        return await ctx.respond(
            embed=EmbedBuilder.create_success_embed(
                ctx,
                author_text=CONST.STRINGS["mod_unbanned_author"],
                description=CONST.STRINGS["mod_unbanned"].format(target.id),
            )
        )

    except (discord.NotFound, discord.HTTPException):
        return await ctx.respond(
            embed=EmbedBuilder.create_warning_embed(
                ctx,
                author_text=CONST.STRINGS["mod_not_banned_author"],
                description=CONST.STRINGS["mod_not_banned"].format(target.id),
            )
        )
