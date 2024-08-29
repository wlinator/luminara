import asyncio
from typing import cast

import discord
from discord.ext import commands

from lib.actionable import async_actionable
from lib.case_handler import create_case
from lib.const import CONST
from lib.exceptions import LumiException
from ui.embeds import Builder


class Warn(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="warn", description="Warn a user")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx: commands.Context[commands.Bot], target: discord.Member, *, reason: str | None = None):
        if not ctx.guild or not ctx.author or not ctx.bot.user:
            raise LumiException

        bot_member = await commands.MemberConverter().convert(ctx, str(ctx.bot.user))
        await async_actionable(target, cast(discord.Member, ctx.author), bot_member)

        output_reason = reason or CONST.STRINGS["mod_no_reason"]

        dm_task = target.send(
            embed=Builder.create_embed(
                theme="info",
                user_name=target.name,
                author_text=CONST.STRINGS["mod_warned_author"],
                description=CONST.STRINGS["mod_warn_dm"].format(
                    target.name,
                    ctx.guild.name,
                    output_reason,
                ),
                hide_name_in_description=True,
            ),
        )

        respond_task = ctx.send(
            embed=Builder.create_embed(
                theme="success",
                user_name=ctx.author.name,
                author_text=CONST.STRINGS["mod_warned_author"],
                description=CONST.STRINGS["mod_warned_user"].format(target.name),
            ),
        )

        create_case_task = create_case(ctx, cast(discord.User, target), "WARN", reason)

        await asyncio.gather(
            dm_task,
            respond_task,
            create_case_task,
            return_exceptions=True,
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Warn(bot))
