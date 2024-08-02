import discord
from typing import Optional
from discord.ext.commands import UserConverter
import asyncio
from lib.embed_builder import EmbedBuilder
from lib.constants import CONST
from modules.moderation.utils.case_handler import create_case


async def warn_user(ctx, target: discord.Member, reason: Optional[str]):
    output_reason = reason or CONST.STRINGS["mod_no_reason"]

    dm_task = target.send(
        embed=EmbedBuilder.create_warning_embed(
            ctx,
            author_text=CONST.STRINGS["mod_warned_author"],
            description=CONST.STRINGS["mod_warn_dm"].format(
                target.name,
                ctx.guild.name,
                output_reason,
            ),
            show_name=False,
        ),
    )

    respond_task = ctx.respond(
        embed=EmbedBuilder.create_success_embed(
            ctx,
            author_text=CONST.STRINGS["mod_warned_author"],
            description=CONST.STRINGS["mod_warned_user"].format(target.name),
        ),
    )

    target_user = await UserConverter().convert(ctx, str(target.id))
    create_case_task = create_case(ctx, target_user, "WARN", reason)

    await asyncio.gather(
        dm_task,
        respond_task,
        create_case_task,
        return_exceptions=True,
    )
