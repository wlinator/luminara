import asyncio
import datetime
from typing import cast

import discord
from discord.ext import commands

import lib.format
from lib.actionable import async_actionable
from lib.case_handler import create_case
from lib.const import CONST
from lib.exceptions import LumiException
from ui.embeds import Builder


class Timeout(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="timeout", aliases=["to"])
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @commands.guild_only()
    async def timeout(
        self,
        ctx: commands.Context[commands.Bot],
        target: discord.Member,
        duration: str,
        reason: str | None = None,
    ) -> None:
        """
        Timeout a user in the guild.

        Parameters
        ----------
        target: discord.Member
            The member to timeout.
        duration: str
            The duration of the timeout. Can be in the format of "1d2h3m4s".
        reason: str | None
            The reason for the timeout. Defaults to None.
        """
        assert ctx.guild
        assert ctx.author
        assert ctx.bot.user

        # Parse duration to minutes and validate
        duration_int = lib.format.format_duration_to_seconds(duration)
        duration_str = lib.format.format_seconds_to_duration_string(duration_int)

        # if longer than 27 days, return LumiException
        if duration_int > 2332800:
            raise LumiException(CONST.STRINGS["mod_timeout_too_long"])

        bot_member = await commands.MemberConverter().convert(ctx, str(ctx.bot.user.id))
        await async_actionable(target, cast(discord.Member, ctx.author), bot_member)

        output_reason = reason or CONST.STRINGS["mod_no_reason"]

        await target.timeout(
            datetime.timedelta(seconds=duration_int),
            reason=CONST.STRINGS["mod_reason"].format(
                ctx.author.name,
                lib.format.shorten(output_reason, 200),
            ),
        )

        dm_task = target.send(
            embed=Builder.create_embed(
                theme="warning",
                user_name=target.name,
                author_text=CONST.STRINGS["mod_timed_out_author"],
                description=CONST.STRINGS["mod_timeout_dm"].format(
                    target.name,
                    ctx.guild.name,
                    duration_str,
                    output_reason,
                ),
                hide_name_in_description=True,
            ),
        )

        respond_task = ctx.send(
            embed=Builder.create_embed(
                theme="success",
                user_name=target.name,
                author_text=CONST.STRINGS["mod_timed_out_author"],
                description=CONST.STRINGS["mod_timed_out_user"].format(target.name),
            ),
        )

        create_case_task = create_case(ctx, cast(discord.User, target), "TIMEOUT", reason, duration_int)

        await asyncio.gather(
            dm_task,
            respond_task,
            create_case_task,
            return_exceptions=True,
        )

    @commands.hybrid_command(name="untimeout", aliases=["ut", "rto"])
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @commands.guild_only()
    async def untimeout(
        self,
        ctx: commands.Context[commands.Bot],
        target: discord.Member,
        reason: str | None = None,
    ) -> None:
        """
        Untimeout a user in the guild.

        Parameters
        ----------
        target: discord.Member
            The member to untimeout.
        reason: str | None
            The reason for the untimeout. Defaults to None.
        """
        assert ctx.guild
        assert ctx.author
        assert ctx.bot.user

        output_reason = reason or CONST.STRINGS["mod_no_reason"]

        try:
            await target.timeout(
                None,
                reason=CONST.STRINGS["mod_reason"].format(
                    ctx.author.name,
                    lib.format.shorten(output_reason, 200),
                ),
            )

            respond_task = ctx.send(
                embed=Builder.create_embed(
                    theme="success",
                    user_name=ctx.author.name,
                    author_text=CONST.STRINGS["mod_untimed_out_author"],
                    description=CONST.STRINGS["mod_untimed_out"].format(target.name),
                ),
            )

            target_user = await commands.UserConverter().convert(ctx, str(target.id))
            create_case_task = create_case(ctx, target_user, "UNTIMEOUT", reason)
            await asyncio.gather(respond_task, create_case_task, return_exceptions=True)

        except discord.HTTPException:
            await ctx.send(
                embed=Builder.create_embed(
                    theme="warning",
                    user_name=ctx.author.name,
                    author_text=CONST.STRINGS["mod_not_timed_out_author"],
                    description=CONST.STRINGS["mod_not_timed_out"].format(target.name),
                ),
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Timeout(bot))
