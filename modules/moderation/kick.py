import asyncio
from typing import cast

import discord
from discord.ext import commands

import lib.format
from lib.actionable import async_actionable
from lib.case_handler import create_case
from lib.const import CONST
from ui.embeds import Builder


class Kick(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="kick", description="Kick a user")
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx: commands.Context[commands.Bot], target: discord.Member, *, reason: str | None = None):
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
                    author_text=CONST.STRINGS["mod_kicked_author"],
                    description=CONST.STRINGS["mod_kick_dm"].format(
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

        await target.kick(
            reason=CONST.STRINGS["mod_reason"].format(
                ctx.author.name,
                lib.format.shorten(output_reason, 200),
            ),
        )

        respond_task = ctx.send(
            embed=Builder.create_embed(
                theme="success",
                user_name=ctx.author.name,
                author_text=CONST.STRINGS["mod_kicked_author"],
                description=CONST.STRINGS["mod_kicked_user"].format(target.name),
                footer_text=CONST.STRINGS["mod_dm_sent"] if dm_sent else CONST.STRINGS["mod_dm_not_sent"],
            ),
        )

        create_case_task = create_case(ctx, cast(discord.User, target), "KICK", reason)
        await asyncio.gather(respond_task, create_case_task, return_exceptions=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Kick(bot))
