import asyncio
from typing import Dict, Optional

import discord
from discord.ext import commands

from lib.const import CONST
from ui.embeds import builder
from ui.views.introduction import (
    IntroductionFinishButtons,
    IntroductionStartButtons,
)


class Introduction(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="introduction",
        aliases=["intro"],
        usage="introduction",
    )
    async def introduction(self, ctx: commands.Context[commands.Bot]) -> None:
        guild: Optional[discord.Guild] = self.bot.get_guild(
            CONST.INTRODUCTIONS_GUILD_ID,
        )
        member: Optional[discord.Member] = (
            guild.get_member(ctx.author.id) if guild else None
        )

        if not guild or not member:
            await ctx.send(
                embed=builder.create_embed(
                    theme="error",
                    user_name=ctx.author.name,
                    author_text=CONST.STRINGS["intro_no_guild_author"],
                    description=CONST.STRINGS["intro_no_guild"],
                    footer_text=CONST.STRINGS["intro_service_name"],
                ),
            )
            return

        question_mapping: Dict[str, str] = CONST.INTRODUCTIONS_QUESTION_MAPPING
        channel: Optional[discord.abc.GuildChannel] = guild.get_channel(
            CONST.INTRODUCTIONS_CHANNEL_ID,
        )

        if not channel or isinstance(
            channel,
            (discord.ForumChannel, discord.CategoryChannel),
        ):
            await ctx.send(
                embed=builder.create_embed(
                    theme="error",
                    user_name=ctx.author.name,
                    author_text=CONST.STRINGS["intro_no_channel_author"],
                    description=CONST.STRINGS["intro_no_channel"],
                    footer_text=CONST.STRINGS["intro_service_name"],
                ),
            )
            return

        view: IntroductionStartButtons | IntroductionFinishButtons = (
            IntroductionStartButtons(ctx)
        )
        await ctx.send(
            embed=builder.create_embed(
                theme="info",
                user_name=ctx.author.name,
                author_text=CONST.STRINGS["intro_service_name"],
                description=CONST.STRINGS["intro_start"].format(channel.mention),
                footer_text=CONST.STRINGS["intro_start_footer"],
            ),
            view=view,
        )

        await view.wait()

        if view.clicked_stop:
            await ctx.send(
                embed=builder.create_embed(
                    theme="error",
                    user_name=ctx.author.name,
                    author_text=CONST.STRINGS["intro_stopped_author"],
                    description=CONST.STRINGS["intro_stopped"],
                    footer_text=CONST.STRINGS["intro_service_name"],
                ),
            )
            return

        if view.clicked_start:

            def check(message: discord.Message) -> bool:
                return message.author == ctx.author and isinstance(
                    message.channel,
                    discord.DMChannel,
                )

        answer_mapping: Dict[str, str] = {}

        for key, question in question_mapping.items():
            await ctx.send(
                embed=builder.create_embed(
                    theme="info",
                    user_name=ctx.author.name,
                    author_text=key,
                    description=question,
                    footer_text=CONST.STRINGS["intro_question_footer"],
                ),
            )

            try:
                answer: discord.Message = await self.bot.wait_for(
                    "message",
                    check=check,
                    timeout=300,
                )
                answer_content: str = answer.content.replace("\n", " ")

                if len(answer_content) > 200:
                    await ctx.send(
                        embed=builder.create_embed(
                            theme="error",
                            user_name=ctx.author.name,
                            author_text=CONST.STRINGS["intro_too_long_author"],
                            description=CONST.STRINGS["intro_too_long"],
                            footer_text=CONST.STRINGS["intro_service_name"],
                        ),
                    )
                    return

                answer_mapping[key] = answer_content

            except asyncio.TimeoutError:
                await ctx.send(
                    embed=builder.create_embed(
                        theme="error",
                        user_name=ctx.author.name,
                        author_text=CONST.STRINGS["intro_timeout_author"],
                        description=CONST.STRINGS["intro_timeout"],
                        footer_text=CONST.STRINGS["intro_service_name"],
                    ),
                )
                return

        description: str = "".join(
            CONST.STRINGS["intro_preview_field"].format(key, value)
            for key, value in answer_mapping.items()
        )

        preview: discord.Embed = builder.create_embed(
            theme="info",
            user_name=ctx.author.name,
            author_text=ctx.author.name,
            author_icon_url=ctx.author.display_avatar.url,
            description=description,
            footer_text=CONST.STRINGS["intro_content_footer"],
        )
        view = IntroductionFinishButtons(ctx)

        await ctx.send(embed=preview, view=view)
        await view.wait()

        if view.clicked_confirm:
            await channel.send(
                embed=preview,
                content=CONST.STRINGS["intro_content"].format(ctx.author.mention),
            )
            await ctx.send(
                embed=builder.create_embed(
                    theme="info",
                    user_name=ctx.author.name,
                    author_text=CONST.STRINGS["intro_post_confirmation_author"],
                    description=CONST.STRINGS["intro_post_confirmation"].format(
                        channel.mention,
                    ),
                ),
            )
        else:
            await ctx.send(
                embed=builder.create_embed(
                    theme="error",
                    user_name=ctx.author.name,
                    author_text=CONST.STRINGS["intro_stopped_author"],
                    description=CONST.STRINGS["intro_stopped"],
                    footer_text=CONST.STRINGS["intro_service_name"],
                ),
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Introduction(bot))
