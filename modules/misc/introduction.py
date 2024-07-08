import asyncio
from loguru import logger

import discord
from discord.ext import bridge

from config.parser import JsonCache
from lib.interactions.introduction import (
    IntroductionStartButtons,
    IntroductionFinishButtons,
)
from lib.embeds.error import MiscErrors, IntroErrors
from lib.embeds.intro import General, Questions
from typing import Optional, Union

resources = JsonCache.read_json("resources")


async def cmd(self, ctx: bridge.Context) -> None:
    """
    Introduction command for v2 - heavily optimized.

    Args:
        self (LumiBot): The instance of the LumiBot.
        ctx (bridge.Context): The context of the command invocation.
    """
    # For now, this command is only supported in one guild.
    # Therefore, we check if the user is in that guild.
    guild: Optional[discord.Guild] = self.client.get_guild(
        int(resources["guild_specific"]["guild_id"])
    )

    if guild is None:
        await ctx.respond(embed=MiscErrors.intro_no_guild(ctx))
        return

    # A list of questions and corresponding field names
    # This won't be hardcoded in the future (db update)
    question_mapping: dict[str, str] = resources["guild_specific"]["question_mapping"]

    # channel = await self.client.convert_to_text_channel(
    #     ctx, int(resources["guild_specific"]["intro_channel_id"])
    # )
    channel: Optional[discord.abc.GuildChannel] = guild.get_channel(int(resources["guild_specific"]["intro_channel_id"]))    

    if channel is None or isinstance(channel, discord.ForumChannel) or isinstance(channel, discord.CategoryChannel):
        await ctx.respond(embed=IntroErrors.intro_no_channel(ctx))
        return

    view = IntroductionStartButtons(ctx)
    await ctx.respond(embed=General.start(ctx, channel), view=view)
    await view.wait()

    if view.clickedStop:
        await ctx.send(embed=General.clicked_stop(ctx))
        return

    elif view.clickedStart:

        def check(message: discord.Message) -> bool:
            return message.author == ctx.author and isinstance(
                message.channel, discord.DMChannel
            )

        answer_mapping: dict[str, str] = {}

        for key, question in question_mapping.items():
            await ctx.send(embed=Questions.question(ctx, question))

            try:
                answer: discord.Message = await self.client.wait_for(
                    "message", check=check, timeout=120
                )
                answer_mapping[key] = answer.content.replace("\n", " ")

                if len(answer_mapping[key]) > 200:
                    await ctx.send(embed=IntroErrors.too_long(ctx))
                    return

            except asyncio.TimeoutError:
                await ctx.send(embed=IntroErrors.timeout(ctx))
                return

        # Generate a preview of the introduction, and send it on confirmation.
        preview: discord.Embed = General.preview(ctx, answer_mapping)
        view = IntroductionFinishButtons(ctx)

        await ctx.send(embed=preview, view=view)
        await view.wait()

        if view.clickedConfirm:
            await channel.send(
                embed=preview, content=f"Introduction by {ctx.author.mention}"
            )
            await ctx.send(embed=General.post_confirmation(ctx, channel))

            logger.debug(
                f"Introduction by {ctx.author.name} was submitted in guild {guild.name} ({guild.id})."
            )
            return

        else:
            await ctx.send(embed=General.clicked_stop(ctx))
            return
