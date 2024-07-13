import asyncio

import discord
from discord.ext import bridge

from lib.interactions.introduction import (
    IntroductionStartButtons,
    IntroductionFinishButtons,
)
from typing import Optional
from lib.constants import CONST
from lib.embed_builder import EmbedBuilder


async def cmd(self, ctx: bridge.Context) -> None:
    guild: Optional[discord.Guild] = self.client.get_guild(CONST.KRC_GUILD_ID)
    member = guild.get_member(ctx.author.id) if guild else None

    if guild is None or member is None:
        await ctx.respond(
            embed=EmbedBuilder.create_error_embed(
                ctx,
                author_text=CONST.STRINGS["intro_no_guild_author"],
                description=CONST.STRINGS["intro_no_guild"],
                footer_text=CONST.STRINGS["intro_service_name"],
            )
        )
        return

    question_mapping: dict[str, str] = CONST.KRC_QUESTION_MAPPING
    channel: Optional[discord.abc.GuildChannel] = guild.get_channel(
        CONST.KRC_INTRO_CHANNEL_ID
    )

    if (
        channel is None
        or isinstance(channel, discord.ForumChannel)
        or isinstance(channel, discord.CategoryChannel)
    ):
        await ctx.respond(
            embed=EmbedBuilder.create_error_embed(
                ctx,
                author_text=CONST.STRINGS["intro_no_channel_author"],
                description=CONST.STRINGS["intro_no_channel"],
                footer_text=CONST.STRINGS["intro_service_name"],
            )
        )
        return

    view = IntroductionStartButtons(ctx)
    # await ctx.respond(embed=General.start(ctx, channel), view=view)
    await ctx.respond(
        embed=EmbedBuilder.create_embed(
            ctx,
            author_text=CONST.STRINGS["intro_service_name"],
            description=CONST.STRINGS["intro_start"].format(channel.mention),
            footer_text=CONST.STRINGS["intro_start_footer"],
        ),
        view=view,
    )
    await view.wait()

    if view.clickedStop:
        await ctx.send(
            embed=EmbedBuilder.create_embed(
                ctx,
                author_text=CONST.STRINGS["intro_stopped_author"],
                description=CONST.STRINGS["intro_stopped"],
            )
        )
        return

    elif view.clickedStart:

        def check(message: discord.Message) -> bool:
            return message.author == ctx.author and isinstance(
                message.channel, discord.DMChannel
            )

        answer_mapping: dict[str, str] = {}

        for key, question in question_mapping.items():
            await ctx.send(
                embed=EmbedBuilder.create_embed(
                    ctx,
                    author_text=key,
                    description=question,
                    footer_text=CONST.STRINGS["intro_question_footer"],
                )
            )

            try:
                answer: discord.Message = await self.client.wait_for(
                    "message", check=check, timeout=120
                )
                answer_mapping[key] = answer.content.replace("\n", " ")

                if len(answer_mapping[key]) > 200:
                    await ctx.send(
                        embed=EmbedBuilder.create_error_embed(
                            ctx,
                            author_text=CONST.STRINGS["intro_too_long_author"],
                            description=CONST.STRINGS["intro_too_long"],
                            footer_text=CONST.STRINGS["intro_service_name"],
                        )
                    )
                    return

            except asyncio.TimeoutError:
                await ctx.send(
                    embed=EmbedBuilder.create_error_embed(
                        ctx,
                        author_text=CONST.STRINGS["intro_timeout_author"],
                        description=CONST.STRINGS["intro_timeout"],
                        footer_text=CONST.STRINGS["intro_service_name"],
                    )
                )
                return

        # preview: discord.Embed = General.preview(ctx, answer_mapping)
        description = ""
        for key, value in answer_mapping.items():
            description += CONST.STRINGS["intro_preview_field"].format(key, value)

        preview = EmbedBuilder.create_embed(
            ctx,
            author_text=ctx.author.name,
            author_icon_url=ctx.author.display_avatar.url,
            description=description,
            footer_text=CONST.STRINGS["intro_service_name"],
        )
        view = IntroductionFinishButtons(ctx)

        await ctx.send(embed=preview, view=view)
        await view.wait()

        if view.clickedConfirm:
            await channel.send(
                embed=preview, content=CONST.STRINGS["intro_content"].format(ctx.author.mention)
            )
            await ctx.send(
                embed=EmbedBuilder.create_embed(
                    ctx,
                    description=CONST.STRINGS["intro_post_confirmation"].format(
                        channel.mention
                    ),
                )
            )
            return

        else:
            await ctx.send(
                embed=EmbedBuilder.create_embed(
                    ctx,
                    author_text=CONST.STRINGS["intro_stopped_author"],
                    description=CONST.STRINGS["intro_stopped"],
                )
            )
            return
