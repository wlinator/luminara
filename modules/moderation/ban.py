import asyncio
import contextlib
from typing import cast

import discord
from discord.ext import commands

import lib.format
from lib.actionable import async_actionable
from lib.case_handler import create_case
from lib.const import CONST
from ui.embeds import Builder


class Ban(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ban.usage = lib.format.generate_usage(self.ban)
        self.unban.usage = lib.format.generate_usage(self.unban)

    @commands.hybrid_command(name="ban", aliases=["b"])
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(
        self,
        ctx: commands.Context[commands.Bot],
        target: discord.Member | discord.User,
        *,
        reason: str | None = None,
    ) -> None:
        """
        Ban a user from the guild.

        Parameters
        ----------
        target: discord.Member | discord.User
            The user to ban.
        reason: str | None
            The reason for the ban.
        """
        assert ctx.guild
        assert ctx.author
        assert ctx.bot.user

        output_reason = reason or CONST.STRINGS["mod_no_reason"]
        formatted_reason = CONST.STRINGS["mod_reason"].format(
            ctx.author.name,
            lib.format.shorten(output_reason, 200),
        )

        dm_sent = False
        if isinstance(target, discord.Member):
            bot_member = await commands.MemberConverter().convert(ctx, str(ctx.bot.user.id))
            await async_actionable(target, cast(discord.Member, ctx.author), bot_member)

            with contextlib.suppress(discord.HTTPException, discord.Forbidden):
                await target.send(
                    embed=Builder.create_embed(
                        theme="warning",
                        user_name=target.name,
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

        await ctx.guild.ban(target, reason=formatted_reason)

        embed = Builder.create_embed(
            theme="success",
            user_name=ctx.author.name,
            author_text=CONST.STRINGS["mod_banned_author"],
            description=CONST.STRINGS["mod_banned_user"].format(target.name),
        )
        if isinstance(target, discord.Member):
            embed.set_footer(text=CONST.STRINGS["mod_dm_sent"] if dm_sent else CONST.STRINGS["mod_dm_not_sent"])

        await asyncio.gather(
            ctx.send(embed=embed),
            create_case(ctx, cast(discord.User, target), "BAN", reason),
            return_exceptions=True,
        )

    @commands.hybrid_command(name="unban")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
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
                    description=CONST.STRINGS["mod_unbanned"].format(target.name),
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
