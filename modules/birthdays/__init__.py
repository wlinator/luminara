import asyncio
import logging
import random

import discord
from discord.ext import commands, tasks, bridge

from config.parser import JsonCache
from lib import time, checks
from lib.embeds.error import BdayErrors
from modules.birthdays import upcoming, birthday
from services.Birthday import Birthday
from services.GuildConfig import GuildConfig

logs = logging.getLogger('Racu.Core')
data = JsonCache.read_json("birthday")
month_mapping = data["month_mapping"]
messages = data["birthday_messages"]


class Birthdays(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.daily_birthday_check.start()

    @bridge.bridge_command(
        name="birthday",
        aliases=["bday"],
        description="Set your birthday.",
        guild_only=True
    )
    @commands.guild_only()
    @checks.birthdays_enabled()
    @checks.allowed_in_channel()
    async def set_birthday(self, ctx, month: str, *, day: int):
        """
        Set your birthday. You can use abbreviations for months, like "jan" and "nov".
        Racu reads only the first three characters to decide the month.
        """

        month_name = await birthday.get_month_name(month, month_mapping)
        month_index = await birthday.get_month_index(month_name, month_mapping)
        await birthday.cmd(ctx, month_name, month_index, day)

    @set_birthday.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.respond(embed=BdayErrors.missing_arg(ctx))
        elif isinstance(error, commands.BadArgument):
            await ctx.respond(embed=BdayErrors.bad_month(ctx))

    @bridge.bridge_command(
        name="upcoming",
        aliases=["birthdayupcoming", "ub"],
        description="See upcoming birthdays!",
        guild_only=True
    )
    @commands.guild_only()
    @checks.birthdays_enabled()
    @checks.allowed_in_channel()
    async def upcoming_birthdays(self, ctx):
        """
        Shows the upcoming birthdays in this server.
        """

        await upcoming.cmd(ctx)

    @tasks.loop(hours=23, minutes=55)
    async def daily_birthday_check(self):

        wait_time = time.seconds_until(7, 0)
        logs.info(f"[BirthdayHandler] Waiting until 7 AM Eastern for daily check: {round(wait_time)}s")
        await asyncio.sleep(wait_time)

        embed = discord.Embed(color=discord.Color.embed_background())
        embed.set_image(url="https://media1.tenor.com/m/NXvU9jbBUGMAAAAC/fireworks.gif")

        for user_id, guild_id in Birthday.get_birthdays_today():
            try:
                guild = await self.client.fetch_guild(guild_id)
                member = await guild.fetch_member(user_id)
                guild_config = GuildConfig(guild.id)

                if not guild_config.birthday_channel_id:
                    logs.info(f"[BirthdayHandler] Guild with ID {guild.id} skipped: no birthday channel defined.")
                    return

                message = random.choice(messages)
                embed.description = message.format(member.name)
                channel = await self.client.get_or_fetch_channel(guild, guild_config.birthday_channel_id)
                await channel.send(embed=embed, content=member.mention)
                logs.info(f"[BirthdayHandler] Success! user/guild/channel ID: {member.id}/{guild.id}/{channel.id}")

            except Exception as error:
                logs.info(f"[BirthdayHandler] Skipped processing user/guild {user_id}/{guild_id}")

            # wait one second to avoid rate limits
            await asyncio.sleep(1)


def setup(client):
    client.add_cog(Birthdays(client))
