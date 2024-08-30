import asyncio
from typing import cast

import discord
from discord.ext import commands

import lib.format
from lib.actionable import async_actionable
from lib.case_handler import create_case
from lib.const import CONST
from ui.embeds import Builder


@commands.has_permissions(ban_members=True)
class Ban(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="ban")
    async def ban(self, ctx: commands.Context[commands.Bot], target: discord.User, *, reason: str | None = None):
        """
        Ban a user from the guild.

        Parameters
        ----------
        target: discord.User
            The user to ban.
        reason: str | None
            The reason for the ban.
        """
        assert ctx.guild
        assert ctx.author
        assert ctx.bot.user

        # see if user is in guild
        member = await commands.MemberConverter().convert(ctx, str(target.id))
        output_reason = reason or CONST.STRINGS["mod_no_reason"]

        # member -> user is in the guild, check role hierarchy
        if member:
            bot_member = await commands.MemberConverter().convert(ctx, str(ctx.bot.user.id))
            await async_actionable(member, cast(discord.Member, ctx.author), bot_member)

            try:
                await member.send(
                    embed=Builder.create_embed(
                        theme="warning",
                        user_name=member.name,
                        author_text=CONST.STRINGS["mod_banned_author"],
                        description=CONST.STRINGS["mod_ban_dm"].format(
                            target.name,
                            ctx.guild.name,
                            output_reason,
                        ),
                        hide_name_in_description=True,
                    ),
                )
                dm_sent = True

            except (discord.HTTPException, discord.Forbidden):
                dm_sent = False

            await member.ban(
                reason=CONST.STRINGS["mod_reason"].format(
                    ctx.author.name,
                    lib.format.shorten(output_reason, 200),
                ),
                delete_message_seconds=86400,
            )

            respond_task = ctx.send(
                embed=Builder.create_embed(
                    theme="success",
                    user_name=ctx.author.name,
                    author_text=CONST.STRINGS["mod_banned_author"],
                    description=CONST.STRINGS["mod_banned_user"].format(target.id),
                    footer_text=CONST.STRINGS["mod_dm_sent"] if dm_sent else CONST.STRINGS["mod_dm_not_sent"],
                ),
            )
            create_case_task = create_case(ctx, target, "BAN", reason)
            await asyncio.gather(respond_task, create_case_task, return_exceptions=True)

        # not a member in this guild, so ban right away
        else:
            await ctx.guild.ban(
                target,
                reason=CONST.STRINGS["mod_reason"].format(
                    ctx.author.name,
                    lib.format.shorten(output_reason, 200),
                ),
            )

            respond_task = ctx.send(
                embed=Builder.create_embed(
                    theme="success",
                    user_name=ctx.author.name,
                    author_text=CONST.STRINGS["mod_banned_author"],
                    description=CONST.STRINGS["mod_banned_user"].format(target.id),
                ),
            )
            create_case_task = create_case(ctx, target, "BAN", reason)
            await asyncio.gather(respond_task, create_case_task)

    @commands.hybrid_command(name="unban")
    async def unban(
        self,
        ctx: commands.Context[commands.Bot],
        target: discord.User,
        *,
        reason: str | None = None,
    ) -> None:
        """
        Unban a user from the guild.

        Parameters
        ----------
        target: discord.User
            The user to unban.
        reason: str | None
            The reason for the unban.
        """
        assert ctx.guild
        assert ctx.author
        assert ctx.bot.user

        output_reason = reason or CONST.STRINGS["mod_no_reason"]

        try:
            await ctx.guild.unban(
                target,
                reason=CONST.STRINGS["mod_reason"].format(
                    ctx.author.name,
                    lib.format.shorten(output_reason, 200),
                ),
            )

            respond_task = ctx.send(
                embed=Builder.create_embed(
                    theme="success",
                    user_name=ctx.author.name,
                    author_text=CONST.STRINGS["mod_unbanned_author"],
                    description=CONST.STRINGS["mod_unbanned"].format(target.id),
                ),
            )
            create_case_task = create_case(ctx, target, "UNBAN", reason)
            await asyncio.gather(respond_task, create_case_task)

        except (discord.NotFound, discord.HTTPException):
            await ctx.send(
                embed=Builder.create_embed(
                    theme="error",
                    user_name=ctx.author.name,
                    author_text=CONST.STRINGS["mod_not_banned_author"],
                    description=CONST.STRINGS["mod_not_banned"].format(target.id),
                ),
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ban(bot))
