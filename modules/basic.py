import asyncio
import logging
import os
import subprocess

import discord
from discord.ext import commands

from sb_tools import interaction, embeds, universal

racu_logs = logging.getLogger('Racu.Core')


class BasicCog(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot

    @commands.slash_command(
        name="ping",
        description="Show the bot's latency.",
        guild_only=True
    )
    @commands.check(universal.channel_check)
    async def ping(self, ctx):
        ping = round(self.bot.latency * 1000, 2)
        await ctx.respond(f"SB latency: {ping} ms")

    @commands.slash_command(
        name="restart",
        description="Restart and update the bot - owner only command.",
        guild_only=True
    )
    @commands.check(universal.owner_check)
    async def restart(self, ctx):

        try:
            logs_dir = "logs"
            for filename in os.listdir(logs_dir):
                file_path = os.path.join(logs_dir, filename)
                if os.path.isfile(file_path):
                    with open(file_path, "w"):
                        pass

        except Exception as err:
            racu_logs.error("Failed to delete logs: ", err)

        await ctx.respond(content="Restarting..", ephemeral=True)

        try:
            racu_logs.info(subprocess.check_output(["/bin/bash", "racu_update.sh"]))
        except subprocess.CalledProcessError as e:
            racu_logs.debug(e.output.decode())

    @commands.slash_command(
        name="intro",
        guild_only=False,
        description="This command can only be done in DMs."
    )
    @commands.dm_only()
    async def intro(self, ctx):
        guild_id = 719227135151046699
        channel_id = 973619250507972618
        muted_role_id = 754895743151505489

        nickname = None
        age = None
        location = None
        pronouns = None
        likes = None
        dislikes = None
        languages = None
        sexuality = None
        relationship_status = None
        extra = None

        guild = self.bot.get_guild(guild_id)
        member = await guild.fetch_member(ctx.author.id)
        if member and discord.utils.get(member.roles, id=muted_role_id):
            em = discord.Embed(description="You're muted in the Rave Cave. You can't perform this command.",
                               color=0xadcca6)
            await ctx.respond(embed=em)
            racu_logs.warning(f"{ctx.author.name} couldn't do the intro command: Muted in the Race Cave")
            return

        elif member and not discord.utils.get(member.roles, id=719995790319157279):
            em = discord.Embed(description="It seems that you don't have permission to do that!")
            await ctx.respond(embed=em)
            racu_logs.warning(f"{ctx.author.name} couldn't do the intro command: No Permissions")
            return

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
            racu_logs.debug(f"{ctx.author.name} clicked Short Intro")

            # START NICKNAME
            await ctx.send(embed=embeds.simple_question_first("How would you like to be identified in the server?"))

            try:
                nickname_message = await self.bot.wait_for('message', check=check, timeout=120)
                nickname = nickname_message.content
                if len(nickname) > 100:
                    nickname = nickname[:100]
                nickname = nickname.replace("\n", " ")
                racu_logs.debug(f"{ctx.author.name} nickname: {nickname}")

                # START AGE
                await ctx.send(embed=embeds.simple_question_5("How old are you?"),
                               content=f"Recorded answer: {nickname}")

                try:
                    age_message = await self.bot.wait_for('message', check=check, timeout=120)
                    age = age_message.content
                    if len(age) > 5:
                        age = age[:5]
                    age = age.replace("\n", " ")
                    racu_logs.debug(f"{ctx.author.name} age: {age}")

                    # START LOCATION
                    view = interaction.LocationOptions(ctx)
                    await ctx.send(embed=embeds.simple_question_none("Where do you live?"),
                                   view=view,
                                   content=f"Recorded answer: {age}")

                    await view.wait()
                    location = view.location

                    if not view.location:
                        await ctx.send(embed=embeds.no_time())
                        return

                    racu_logs.debug(f"{ctx.author.name} location: {location}")

                    # START PRONOUNS
                    await ctx.send(
                        embed=embeds.simple_question_30("What are your preferred pronouns?"),
                        content=f"Recorded answer: {location}")

                    try:
                        pronouns_message = await self.bot.wait_for('message', check=check, timeout=120)
                        pronouns = pronouns_message.content
                        if len(pronouns) > 30:
                            pronouns = pronouns[:30]
                        pronouns = pronouns.replace("\n", " ")
                        racu_logs.debug(f"{ctx.author.name} pronouns: {pronouns}")

                        # START LIKES
                        await ctx.send(embed=embeds.simple_question_300("Likes & interests"),
                                       content=f"Recorded answer: {pronouns}")

                        try:
                            likes_message = await self.bot.wait_for('message', check=check, timeout=300)
                            likes = likes_message.content
                            if len(likes) > 300:
                                likes = likes[:300]
                            likes = likes.replace("\n", " ")
                            racu_logs.debug(f"{ctx.author.name} likes: {likes}")

                            # START DISLIKES
                            await ctx.send(embed=embeds.simple_question_300("Dislikes"),
                                           content=f"Recorded answer: {likes}")

                            try:
                                dislikes_message = await self.bot.wait_for('message', check=check, timeout=300)
                                dislikes = dislikes_message.content
                                if len(dislikes) > 300:
                                    dislikes = dislikes[:300]
                                dislikes = dislikes.replace("\n", " ")
                                racu_logs.debug(f"{ctx.author.name} dislikes: {dislikes}")

                                # POST EXAMPLE EMBED AND FINAL IF APPROVED
                                em = embeds.final_embed_short(ctx, nickname, age, location, pronouns, likes, dislikes)

                                view = interaction.Confirm(ctx)
                                await ctx.send(embed=em, content=f"Introduction of <@{ctx.author.id}>", view=view)
                                await view.wait()

                                if view.clickedConfirm:
                                    intro_channel = guild.get_channel(channel_id)
                                    await intro_channel.send(embed=em, content=f"Introduction of <@{ctx.author.id}>")
                                    await ctx.send(embed=embeds.final_confirmation(channel_id))
                                    racu_logs.info(f"{ctx.author.name} Intro Sent")
                                    return
                                else:
                                    await ctx.send(embed=embeds.no_time())
                                    racu_logs.warning(f"{ctx.author.id} Intro Timeout")
                                    return

                            except asyncio.TimeoutError:
                                await ctx.send(embed=embeds.no_time())
                                racu_logs.warning(f"{ctx.author.id} Intro Timeout")
                                return

                        except asyncio.TimeoutError:
                            await ctx.send(embed=embeds.no_time())
                            racu_logs.warning(f"{ctx.author.id} Intro Timeout")
                            return

                    except asyncio.TimeoutError:
                        await ctx.send(embed=embeds.no_time())
                        racu_logs.warning(f"{ctx.author.id} Intro Timeout")
                        return

                except asyncio.TimeoutError:
                    await ctx.send(embed=embeds.no_time())
                    racu_logs.warning(f"{ctx.author.id} Intro Timeout")
                    return

            except asyncio.TimeoutError:
                await ctx.send(embed=embeds.no_time())
                racu_logs.warning(f"{ctx.author.id} Intro Timeout")
                return

        elif view.clickedLong:
            racu_logs.debug(f"{ctx.author.name} clicked Long Intro")

            # START NICKNAME
            await ctx.send(embed=embeds.simple_question_first_extended(
                "How would you like to be identified in the server?"))

            try:
                nickname_message = await self.bot.wait_for('message', check=check, timeout=120)
                nickname = nickname_message.content
                if len(nickname) > 100:
                    nickname = nickname[:100]
                nickname = nickname.replace("\n", " ")
                racu_logs.debug(f"{ctx.author.name} nickname: {nickname}")

                # START AGE
                await ctx.send(embed=embeds.simple_question_5("How old are you?"),
                               content=f"Recorded answer: {nickname}")

                try:
                    age_message = await self.bot.wait_for('message', check=check, timeout=120)
                    age = age_message.content
                    if len(age) > 5:
                        age = age[:5]
                    age = age.replace("\n", " ")
                    racu_logs.debug(f"{ctx.author.name} age: {age}")

                    # START LOCATION
                    view = interaction.LocationOptions(ctx)
                    await ctx.send(embed=embeds.simple_question_none("Where do you live?"),
                                   view=view,
                                   content=f"Recorded answer: {age}")

                    await view.wait()
                    location = view.location

                    if not view.location:
                        await ctx.send(embed=embeds.no_time())
                        return

                    racu_logs.debug(f"{ctx.author.name} location: {location}")

                    # START LANGUAGES
                    await ctx.send(
                        embed=embeds.simple_question_100("Which languages do you speak?"),
                        content=f"Recorded answer: {location}"
                    )

                    try:
                        languages_message = await self.bot.wait_for('message', check=check, timeout=200)
                        languages = languages_message.content
                        if len(languages) > 30:
                            languages = languages[:30]
                        languages = languages.replace("\n", " ")
                        racu_logs.debug(f"{ctx.author.name} languages: {languages}")

                        # START PRONOUNS
                        await ctx.send(
                            embed=embeds.simple_question_30("What are your preferred pronouns?"),
                            content=f"Recorded answer: {languages}")

                        try:
                            pronouns_message = await self.bot.wait_for('message', check=check, timeout=120)
                            pronouns = pronouns_message.content
                            if len(pronouns) > 30:
                                pronouns = pronouns[:30]
                            pronouns = pronouns.replace("\n", " ")
                            racu_logs.debug(f"{ctx.author.name} pronouns: {pronouns}")

                            # START SEXUALITY
                            await ctx.send(
                                embed=embeds.simple_question_30("What's your sexuality?"),
                                content=f"Recorded answer: {pronouns}")

                            try:
                                sexuality_message = await self.bot.wait_for('message', check=check, timeout=120)
                                sexuality = sexuality_message.content
                                if len(sexuality) > 30:
                                    sexuality = sexuality[:30]
                                sexuality = sexuality.replace("\n", " ")
                                racu_logs.debug(f"{ctx.author.name} sexuality: {sexuality}")

                                # START RELATIONSHIP_STATUS
                                await ctx.send(
                                    embed=embeds.simple_question_30("What's your current relationship status?"),
                                    content=f"Recorded answer: {sexuality}")

                                try:
                                    relationship_status_message = await self.bot.wait_for('message', check=check,
                                                                                          timeout=120)
                                    relationship_status = relationship_status_message.content
                                    if len(relationship_status) > 30:
                                        relationship_status = relationship_status[:30]
                                    relationship_status = relationship_status.replace("\n", " ")
                                    racu_logs.debug(f"{ctx.author.name} relationship_status: {relationship_status}")

                                    # START LIKES
                                    await ctx.send(embed=embeds.simple_question_300("Likes & interests"),
                                                   content=f"Recorded answer: {relationship_status}")

                                    try:
                                        likes_message = await self.bot.wait_for('message', check=check, timeout=300)
                                        likes = likes_message.content
                                        if len(likes) > 300:
                                            likes = likes[:300]
                                        likes = likes.replace("\n", " ")
                                        racu_logs.debug(f"{ctx.author.name} likes: {likes}")

                                        # START DISLIKES
                                        await ctx.send(embed=embeds.simple_question_300("Dislikes"),
                                                       content=f"Recorded answer: {likes}")

                                        try:
                                            dislikes_message = await self.bot.wait_for('message', check=check,
                                                                                       timeout=300)
                                            dislikes = dislikes_message.content
                                            if len(dislikes) > 300:
                                                dislikes = dislikes[:300]
                                            dislikes = dislikes.replace("\n", " ")
                                            racu_logs.debug(f"{ctx.author.name} dislikes: {dislikes}")

                                            # START EXTRA
                                            await ctx.send(embed=embeds.simple_question_300(
                                                "EXTRAS: job status, zodiac sign, hobbies, etc. "
                                                "Tell us about yourself!"),
                                                content=f"Recorded answer: {dislikes}")

                                            try:
                                                extra_message = await self.bot.wait_for('message', check=check,
                                                                                        timeout=300)
                                                extra = extra_message.content
                                                if len(extra) > 300:
                                                    extra = extra[:300]
                                                extra = extra.replace("\n", " ")
                                                racu_logs.debug(f"{ctx.author.name} extra: {extra}")

                                                # POST EXAMPLE EMBED AND FINAL IF APPROVED
                                                em = embeds.final_embed_extended(ctx, nickname, age, location,
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
                                                    await ctx.send(embed=embeds.final_confirmation(channel_id))
                                                    racu_logs.info(f"{ctx.author.name} Intro Sent")
                                                    return
                                                else:
                                                    await ctx.send(embed=embeds.no_time())
                                                    racu_logs.warning(f"{ctx.author.id} Intro Timeout")
                                                    return

                                            except asyncio.TimeoutError:
                                                await ctx.send(embed=embeds.no_time())
                                                racu_logs.warning(f"{ctx.author.id} Intro Timeout")
                                                return

                                        except asyncio.TimeoutError:
                                            await ctx.send(embed=embeds.no_time())
                                            racu_logs.warning(f"{ctx.author.id} Intro Timeout")
                                            return

                                    except asyncio.TimeoutError:
                                        await ctx.send(embed=embeds.no_time())
                                        racu_logs.warning(f"{ctx.author.id} Intro Timeout")
                                        return

                                except asyncio.TimeoutError:
                                    await ctx.send(embed=embeds.no_time())
                                    racu_logs.warning(f"{ctx.author.id} Intro Timeout")
                                    return

                            except asyncio.TimeoutError:
                                await ctx.send(embed=embeds.no_time())
                                racu_logs.warning(f"{ctx.author.id} Intro Timeout")
                                return

                        except asyncio.TimeoutError:
                            await ctx.send(embed=embeds.no_time())
                            racu_logs.warning(f"{ctx.author.id} Intro Timeout")
                            return

                    except asyncio.TimeoutError:
                        await ctx.send(embed=embeds.no_time())
                        racu_logs.warning(f"{ctx.author.id} Intro Timeout")
                        return

                except asyncio.TimeoutError:
                    await ctx.send(embed=embeds.no_time())
                    racu_logs.warning(f"{ctx.author.id} Intro Timeout")
                    return

            except asyncio.TimeoutError:
                await ctx.send(embed=embeds.no_time())
                racu_logs.warning(f"{ctx.author.id} Intro Timeout")
                return
        else:
            await ctx.send(embed=embeds.no_time())
            racu_logs.warning(f"{ctx.author.id} Intro Timeout")
            return


def setup(sbbot):
    sbbot.add_cog(BasicCog(sbbot))
