import asyncio
import logging
import os
import subprocess

import discord
from discord.ext import commands

from lib import interaction, embeds_old, checks

logs = logging.getLogger('Racu.Core')


async def cmd(self, ctx):
    # rewrite this whole command

    guild_id = 719227135151046699
    channel_id = 973619250507972618

    guild = self.client.get_guild(guild_id)

    try:
        member = await guild.fetch_member(ctx.author.id)
    except discord.HTTPException:
        return await ctx.respond("You can't do this command because you're not "
                                 "in a server that supports introductions.")

    embed = discord.Embed(color=0xadcca6,
                          title=f"Hey {ctx.author.name}!",
                          description=f"This command will serve as a questionnaire "
                                      f"for your entry to <#{channel_id}>. Please keep your answers \"PG-13.\"")

    embed.add_field(name="Short intro", value="Click the blue button to use the short form, this one has "
                                              "__6 questions__, which is filled out promptly & contains the "
                                              "most important elements needed to briefly describe you.")

    embed.add_field(name="Extended intro", value="Click the green button to fill out an extended form with "
                                                 "__10 questions__ (including an \"extras\" field where you "
                                                 "can unleash your creativity), this one takes a bit longer "
                                                 "to fill out but gives a more detailed portrayal of you.")

    embed.set_footer(text="Please don't abuse this command.")
    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/719227135151046699/49df8c284382af9dbcfd629c8eadc52c"
                            ".webp?size=96")

    view = interaction.IntroButtons(ctx)
    await ctx.respond(embed=embed, view=view)
    await view.wait()

    def check(message):
        return message.author == ctx.author and isinstance(message.channel, discord.DMChannel)

    if view.clickedShort:
        logs.debug(f"{ctx.author.name} clicked Short Intro")

        # START NICKNAME
        await ctx.send(embed=embeds_old.simple_question_first("How would you like to be identified in the server?"))

        try:
            nickname_message = await self.client.wait_for('message', check=check, timeout=120)
            nickname = nickname_message.content
            if len(nickname) > 100:
                nickname = nickname[:100]
            nickname = nickname.replace("\n", " ")
            logs.debug(f"{ctx.author.name} nickname: {nickname}")

            # START AGE
            await ctx.send(embed=embeds_old.simple_question_5("How old are you?"),
                           content=f"Recorded answer: {nickname}")

            try:
                age_message = await self.client.wait_for('message', check=check, timeout=120)
                age = age_message.content
                if len(age) > 5:
                    age = age[:5]
                age = age.replace("\n", " ")
                logs.debug(f"{ctx.author.name} age: {age}")

                # START LOCATION
                view = interaction.LocationOptions(ctx)
                await ctx.send(embed=embeds_old.simple_question_none("Where do you live?"),
                               view=view,
                               content=f"Recorded answer: {age}")

                await view.wait()
                location = view.location

                if not view.location:
                    await ctx.send(embed=embeds_old.no_time())
                    return

                logs.debug(f"{ctx.author.name} location: {location}")

                # START PRONOUNS
                await ctx.send(
                    embed=embeds_old.simple_question_30("What are your preferred pronouns?"),
                    content=f"Recorded answer: {location}")

                try:
                    pronouns_message = await self.client.wait_for('message', check=check, timeout=120)
                    pronouns = pronouns_message.content
                    if len(pronouns) > 30:
                        pronouns = pronouns[:30]
                    pronouns = pronouns.replace("\n", " ")
                    logs.debug(f"{ctx.author.name} pronouns: {pronouns}")

                    # START LIKES
                    await ctx.send(embed=embeds_old.simple_question_300("Likes & interests"),
                                   content=f"Recorded answer: {pronouns}")

                    try:
                        likes_message = await self.client.wait_for('message', check=check, timeout=300)
                        likes = likes_message.content
                        if len(likes) > 300:
                            likes = likes[:300]
                        likes = likes.replace("\n", " ")
                        logs.debug(f"{ctx.author.name} likes: {likes}")

                        # START DISLIKES
                        await ctx.send(embed=embeds_old.simple_question_300("Dislikes"),
                                       content=f"Recorded answer: {likes}")

                        try:
                            dislikes_message = await self.client.wait_for('message', check=check, timeout=300)
                            dislikes = dislikes_message.content
                            if len(dislikes) > 300:
                                dislikes = dislikes[:300]
                            dislikes = dislikes.replace("\n", " ")
                            logs.debug(f"{ctx.author.name} dislikes: {dislikes}")

                            # POST EXAMPLE EMBED AND FINAL IF APPROVED
                            em = embeds_old.final_embed_short(ctx, nickname, age, location, pronouns, likes, dislikes)

                            view = interaction.Confirm(ctx)
                            await ctx.send(embed=em, content=f"Introduction of <@{ctx.author.id}>", view=view)
                            await view.wait()

                            if view.clickedConfirm:
                                intro_channel = guild.get_channel(channel_id)
                                await intro_channel.send(embed=em, content=f"Introduction of <@{ctx.author.id}>")
                                await ctx.send(embed=embeds_old.final_confirmation(channel_id))
                                logs.info(f"[CommandHandler] {ctx.author.name} introduction was submitted.")
                                return
                            else:
                                await ctx.send(embed=embeds_old.no_time())
                                logs.warning(f"{ctx.author.id} Intro Timeout")
                                return

                        except asyncio.TimeoutError:
                            await ctx.send(embed=embeds_old.no_time())
                            logs.warning(f"{ctx.author.id} Intro Timeout")
                            return

                    except asyncio.TimeoutError:
                        await ctx.send(embed=embeds_old.no_time())
                        logs.warning(f"{ctx.author.id} Intro Timeout")
                        return

                except asyncio.TimeoutError:
                    await ctx.send(embed=embeds_old.no_time())
                    logs.warning(f"{ctx.author.id} Intro Timeout")
                    return

            except asyncio.TimeoutError:
                await ctx.send(embed=embeds_old.no_time())
                logs.warning(f"{ctx.author.id} Intro Timeout")
                return

        except asyncio.TimeoutError:
            await ctx.send(embed=embeds_old.no_time())
            logs.warning(f"{ctx.author.id} Intro Timeout")
            return

    elif view.clickedLong:
        logs.debug(f"{ctx.author.name} clicked Long Intro")

        # START NICKNAME
        await ctx.send(embed=embeds_old.simple_question_first_extended(
            "How would you like to be identified in the server?"))

        try:
            nickname_message = await self.client.wait_for('message', check=check, timeout=120)
            nickname = nickname_message.content
            if len(nickname) > 100:
                nickname = nickname[:100]
            nickname = nickname.replace("\n", " ")
            logs.debug(f"{ctx.author.name} nickname: {nickname}")

            # START AGE
            await ctx.send(embed=embeds_old.simple_question_5("How old are you?"),
                           content=f"Recorded answer: {nickname}")

            try:
                age_message = await self.client.wait_for('message', check=check, timeout=120)
                age = age_message.content
                if len(age) > 5:
                    age = age[:5]
                age = age.replace("\n", " ")
                logs.debug(f"{ctx.author.name} age: {age}")

                # START LOCATION
                view = interaction.LocationOptions(ctx)
                await ctx.send(embed=embeds_old.simple_question_none("Where do you live?"),
                               view=view,
                               content=f"Recorded answer: {age}")

                await view.wait()
                location = view.location

                if not view.location:
                    await ctx.send(embed=embeds_old.no_time())
                    return

                logs.debug(f"{ctx.author.name} location: {location}")

                # START LANGUAGES
                await ctx.send(
                    embed=embeds_old.simple_question_100("Which languages do you speak?"),
                    content=f"Recorded answer: {location}"
                )

                try:
                    languages_message = await self.client.wait_for('message', check=check, timeout=200)
                    languages = languages_message.content
                    if len(languages) > 30:
                        languages = languages[:30]
                    languages = languages.replace("\n", " ")
                    logs.debug(f"{ctx.author.name} languages: {languages}")

                    # START PRONOUNS
                    await ctx.send(
                        embed=embeds_old.simple_question_30("What are your preferred pronouns?"),
                        content=f"Recorded answer: {languages}")

                    try:
                        pronouns_message = await self.client.wait_for('message', check=check, timeout=120)
                        pronouns = pronouns_message.content
                        if len(pronouns) > 30:
                            pronouns = pronouns[:30]
                        pronouns = pronouns.replace("\n", " ")
                        logs.debug(f"{ctx.author.name} pronouns: {pronouns}")

                        # START SEXUALITY
                        await ctx.send(
                            embed=embeds_old.simple_question_30("What's your sexuality?"),
                            content=f"Recorded answer: {pronouns}")

                        try:
                            sexuality_message = await self.client.wait_for('message', check=check, timeout=120)
                            sexuality = sexuality_message.content
                            if len(sexuality) > 30:
                                sexuality = sexuality[:30]
                            sexuality = sexuality.replace("\n", " ")
                            logs.debug(f"{ctx.author.name} sexuality: {sexuality}")

                            # START RELATIONSHIP_STATUS
                            await ctx.send(
                                embed=embeds_old.simple_question_30("What's your current relationship status?"),
                                content=f"Recorded answer: {sexuality}")

                            try:
                                relationship_status_message = await self.client.wait_for('message', check=check,
                                                                                         timeout=120)
                                relationship_status = relationship_status_message.content
                                if len(relationship_status) > 30:
                                    relationship_status = relationship_status[:30]
                                relationship_status = relationship_status.replace("\n", " ")
                                logs.debug(f"{ctx.author.name} relationship_status: {relationship_status}")

                                # START LIKES
                                await ctx.send(embed=embeds_old.simple_question_300("Likes & interests"),
                                               content=f"Recorded answer: {relationship_status}")

                                try:
                                    likes_message = await self.client.wait_for('message', check=check, timeout=300)
                                    likes = likes_message.content
                                    if len(likes) > 300:
                                        likes = likes[:300]
                                    likes = likes.replace("\n", " ")
                                    logs.debug(f"{ctx.author.name} likes: {likes}")

                                    # START DISLIKES
                                    await ctx.send(embed=embeds_old.simple_question_300("Dislikes"),
                                                   content=f"Recorded answer: {likes}")

                                    try:
                                        dislikes_message = await self.client.wait_for('message', check=check,
                                                                                      timeout=300)
                                        dislikes = dislikes_message.content
                                        if len(dislikes) > 300:
                                            dislikes = dislikes[:300]
                                        dislikes = dislikes.replace("\n", " ")
                                        logs.debug(f"{ctx.author.name} dislikes: {dislikes}")

                                        # START EXTRA
                                        await ctx.send(embed=embeds_old.simple_question_300(
                                            "EXTRAS: job status, zodiac sign, hobbies, etc. "
                                            "Tell us about yourself!"),
                                            content=f"Recorded answer: {dislikes}")

                                        try:
                                            extra_message = await self.client.wait_for('message', check=check,
                                                                                       timeout=300)
                                            extra = extra_message.content
                                            if len(extra) > 300:
                                                extra = extra[:300]
                                            extra = extra.replace("\n", " ")
                                            logs.debug(f"{ctx.author.name} extra: {extra}")

                                            # POST EXAMPLE EMBED AND FINAL IF APPROVED
                                            em = embeds_old.final_embed_extended(ctx, nickname, age, location,
                                                                                 languages, pronouns, sexuality,
                                                                                 relationship_status, likes,
                                                                                 dislikes, extra)

                                            view = interaction.Confirm(ctx)
                                            await ctx.send(embed=em, content=f"Introduction of <@{ctx.author.id}>",
                                                           view=view)
                                            await view.wait()

                                            if view.clickedConfirm:
                                                intro_channel = guild.get_channel(channel_id)
                                                await intro_channel.send(embed=em,
                                                                         content=f"Introduction of <@{ctx.author.id}>")
                                                await ctx.send(embed=embeds_old.final_confirmation(channel_id))
                                                logs.info(
                                                    f"[CommandHandler] {ctx.author.name} introduction was submitted.")
                                                return
                                            else:
                                                await ctx.send(embed=embeds_old.no_time())
                                                logs.warning(f"{ctx.author.id} Intro Timeout")
                                                return

                                        except asyncio.TimeoutError:
                                            await ctx.send(embed=embeds_old.no_time())
                                            logs.warning(f"{ctx.author.id} Intro Timeout")
                                            return

                                    except asyncio.TimeoutError:
                                        await ctx.send(embed=embeds_old.no_time())
                                        logs.warning(f"{ctx.author.id} Intro Timeout")
                                        return

                                except asyncio.TimeoutError:
                                    await ctx.send(embed=embeds_old.no_time())
                                    logs.warning(f"{ctx.author.id} Intro Timeout")
                                    return

                            except asyncio.TimeoutError:
                                await ctx.send(embed=embeds_old.no_time())
                                logs.warning(f"{ctx.author.id} Intro Timeout")
                                return

                        except asyncio.TimeoutError:
                            await ctx.send(embed=embeds_old.no_time())
                            logs.warning(f"{ctx.author.id} Intro Timeout")
                            return

                    except asyncio.TimeoutError:
                        await ctx.send(embed=embeds_old.no_time())
                        logs.warning(f"{ctx.author.id} Intro Timeout")
                        return

                except asyncio.TimeoutError:
                    await ctx.send(embed=embeds_old.no_time())
                    logs.warning(f"{ctx.author.id} Intro Timeout")
                    return

            except asyncio.TimeoutError:
                await ctx.send(embed=embeds_old.no_time())
                logs.warning(f"{ctx.author.id} Intro Timeout")
                return

        except asyncio.TimeoutError:
            await ctx.send(embed=embeds_old.no_time())
            logs.warning(f"{ctx.author.id} Intro Timeout")
            return
    else:
        await ctx.send(embed=embeds_old.no_time())
        logs.warning(f"{ctx.author.id} Intro Timeout")
        return