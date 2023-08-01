import asyncio
import calendar
import datetime
import logging
import random

import discord
import pytz
from discord.ext import commands, tasks

from config import json_loader
from data.Birthday import Birthday
from main import strings

racu_logs = logging.getLogger('Racu.Core')

months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

messages = json_loader.load_birthday_messages()


class BirthdayCog(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot
        self.daily_birthday_check.start()

    @commands.slash_command(
        name="birthday",
        description="Set your birthday.",
        guild_only=True
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def set_birthday(self, ctx, *,
                           month: discord.Option(choices=months),
                           day: discord.Option(int)):
        leap_year = 2020
        month_index = months.index(month) + 1
        max_days = calendar.monthrange(leap_year, month_index)[1]

        if not (1 <= day <= max_days):
            return await ctx.respond(strings["birthday_invalid_date"].format(ctx.author.name), ephemeral=True)

        date_str = f"{leap_year}-{month_index:02d}-{day:02d}"
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')

        birthday = Birthday(ctx.author.id)
        birthday.set(date_obj)

        await ctx.respond(strings["birthday_set"].format(ctx.author.name, month, day), ephemeral=True)

    @tasks.loop(hours=23, minutes=55)
    async def daily_birthday_check(self):

        wait_time = BirthdayCog.seconds_until(7, 0)
        racu_logs.info(f"daily_birthday_check(): Waiting until 7 AM Eastern: {wait_time}")
        await asyncio.sleep(wait_time)

        birthday_ids = Birthday.today()

        if birthday_ids:
            channel_id = 741021558172287099
            channel = await self.bot.fetch_channel(channel_id)

            for user_id in birthday_ids:
                user = self.bot.fetch_user(user_id)
                message = random.choice(messages["birthday_messages"])
                await channel.send(message.format(f"<@{user_id}>"))

                racu_logs.info(f"daily_birthday_check(): Sent message for USER ID: {user_id}")

        else:
            racu_logs.info("daily_birthday_check(): No Birthdays Today.")

    @staticmethod
    def seconds_until(hours, minutes):
        eastern_timezone = pytz.timezone('US/Eastern')

        now = datetime.datetime.now(eastern_timezone)

        # Create a datetime object for the given time in the Eastern Timezone
        given_time = datetime.time(hours, minutes)
        future_exec = eastern_timezone.localize(datetime.datetime.combine(now, given_time))

        # If the given time is before the current time, add one day to the future execution time
        if future_exec < now:
            future_exec += datetime.timedelta(days=1)

        # Calculate the time difference in seconds
        seconds_until_execution = (future_exec - now).total_seconds()

        return seconds_until_execution


def setup(sbbot):
    sbbot.add_cog(BirthdayCog(sbbot))
