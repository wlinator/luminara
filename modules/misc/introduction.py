import asyncio
from loguru import logger

import discord

from config.parser import JsonCache
from lib import interaction
from lib.embeds.error import MiscErrors, IntroErrors
from lib.embeds.intro import General, Questions

resources = JsonCache.read_json("resources")


async def cmd(self, ctx: discord.ApplicationContext):
    """
    Introduction command for v2 - heavily optimized.
    """
    """
    For now, this command is only supported in one guild.
    Therefore, we check if the user is in that guild.
    """
    guild = self.client.get_guild(int(resources["guild_specific"]["guild_id"]))

    try:
        _ = await guild.fetch_member(ctx.author.id)
    except discord.HTTPException:
        return await ctx.respond(embed=MiscErrors.intro_no_guild(ctx))
    except AttributeError:
        return await ctx.respond(embed=MiscErrors.intro_no_guild(ctx, client_side=True))

    """
    A list of questions and corresponding field names
    This won't be hardcoded in the future (db update)
    """
    question_mapping = resources["guild_specific"]["question_mapping"]

    channel = await self.client.get_or_fetch_channel(guild, int(resources["guild_specific"]["intro_channel_id"]))
    view = interaction.IntroButtons(ctx)
    await ctx.respond(embed=General.start(ctx, channel), view=view)
    await view.wait()

    if view.clickedStop:
        return await ctx.send(embed=General.clicked_stop(ctx))

    elif view.clickedStart:
        def check(message):
            return message.author == ctx.author and isinstance(message.channel, discord.DMChannel)

        answer_mapping = {}

        for key, question in question_mapping.items():
            await ctx.send(embed=Questions.question(ctx, question))

            try:
                answer = await self.client.wait_for('message', check=check, timeout=120)
                answer_mapping[key] = answer.content.replace("\n", " ")

                if len(answer_mapping[key]) > 200:
                    return await ctx.send(embed=IntroErrors.too_long(ctx))

            except asyncio.TimeoutError:
                return await ctx.send(embed=IntroErrors.timeout(ctx))

        """
        Generate a preview of the introduction, and send it on confirmation.
        """
        preview = General.preview(ctx, answer_mapping)
        view = interaction.Confirm(ctx)

        await ctx.send(embed=preview, view=view)
        await view.wait()

        if view.clickedConfirm:
            await channel.send(embed=preview, content=f"Introduction by {ctx.author.mention}")
            await ctx.send(embed=General.post_confirmation(ctx, channel))

            logger.debug(f"Introduction by {ctx.author.name} was submitted in guild {guild.name} ({guild.id}).")
            return

        else:
            await ctx.send(embed=General.clicked_stop(ctx))
            return
