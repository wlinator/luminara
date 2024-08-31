import asyncio
from typing import cast

import discord
from discord.ext import commands

import lib.format as formatter
from lib.actionable import async_actionable
from lib.case_handler import create_case
from lib.const import CONST
from ui.embeds import Builder


class Softban(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="softban", aliases=["sb"])
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    async def softban(
        self,
        ctx: commands.Context[commands.Bot],
        target: discord.Member,
        *,
        reason: str | None = None,
    ) -> None:
        """
        Softban a user from the guild.

        Parameters
        ----------
        target: discord.Member
            The user to softban.
        reason: str | None
            The reason for the softban. Defaults to None.
        """
        assert ctx.guild
        assert ctx.author
        assert ctx.bot.user

        bot_member = await commands.MemberConverter().convert(ctx, str(ctx.bot.user.id))
        await async_actionable(target, cast(discord.Member, ctx.author), bot_member)

        output_reason = reason or CONST.STRINGS["mod_no_reason"]

        try:
            await target.send(
                embed=Builder.create_embed(
                    theme="warning",
                    user_name=target.name,
                    author_text=CONST.STRINGS["mod_softbanned_author"],
                    description=CONST.STRINGS["mod_softban_dm"].format(
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

        await ctx.guild.ban(
            target,
            reason=CONST.STRINGS["mod_reason"].format(
                ctx.author.name,
                formatter.shorten(output_reason, 200),
            ),
            delete_message_seconds=86400,
        )

        await ctx.guild.unban(
            target,
            reason=CONST.STRINGS["mod_softban_unban_reason"].format(
                ctx.author.name,
            ),
        )

        respond_task = ctx.send(
            embed=Builder.create_embed(
                theme="success",
                user_name=target.name,
                author_text=CONST.STRINGS["mod_softbanned_author"],
                description=CONST.STRINGS["mod_softbanned_user"].format(target.name),
                footer_text=CONST.STRINGS["mod_dm_sent"] if dm_sent else CONST.STRINGS["mod_dm_not_sent"],
            ),
        )

        create_case_task = create_case(ctx, cast(discord.User, target), "SOFTBAN", reason)
        await asyncio.gather(respond_task, create_case_task, return_exceptions=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Softban(bot))
