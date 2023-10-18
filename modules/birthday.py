import asyncio
import calendar
import datetime
import logging
import random

import discord
from discord import default_permissions
from discord.ext import commands, tasks

from config import json_loader
from data.Birthday import Birthday
from main import strings
from utils import time

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

    @commands.slash_command(
        name="override-birthday",
        description="Override a birthday - requires Manage Server.",
        guild_only=True
    )
    @default_permissions(manage_guild=True)
    async def override_birthday(self, ctx, *,
                                user: discord.Option(discord.Member),
                                month: discord.Option(choices=months),
                                day: discord.Option(int)):
        leap_year = 2020
        month_index = months.index(month) + 1
        max_days = calendar.monthrange(leap_year, month_index)[1]

        if not (1 <= day <= max_days):
            return await ctx.respond(strings["birthday_invalid_date"].format(ctx.author.name), ephemeral=True)

        date_str = f"{leap_year}-{month_index:02d}-{day:02d}"
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')

        birthday = Birthday(user.id)
        birthday.set(date_obj)

        await ctx.respond(strings["birthday_override"].format(ctx.author.name, user.name, month, day))

    @tasks.loop(hours=23, minutes=55)
    async def daily_birthday_check(self):

        wait_time = time.seconds_until(7, 0)
        racu_logs.info(f"daily_birthday_check(): Waiting until 7 AM Eastern: {wait_time}")
        await asyncio.sleep(wait_time)

        birthday_ids = Birthday.today()

        if birthday_ids:
            guild_id = 719227135151046699  # Kaiju's Rave Cave
            channel_id = 741021558172287099  # Birthdays channel

            guild = await self.bot.fetch_guild(guild_id)
            channel = await guild.fetch_channel(channel_id)

            for user_id in birthday_ids:

                try:
                    user = await guild.fetch_member(user_id)
                    print(user)

                    message = random.choice(messages["birthday_messages"])
                    await channel.send(message.format(user.mention))

                    racu_logs.info(f"daily_birthday_check(): Sent message for USER ID: {user_id}")

                except discord.HTTPException:
                    racu_logs.info(f"daily_birthday_check(): Not sent because USER ID {user_id} not in Guild.")

                except Exception as err:
                    racu_logs.error(f"daily_birthday_check(): Something went wrong: {err}")

        else:
            racu_logs.info("daily_birthday_check(): No Birthdays Today.")


def setup(sbbot):
    sbbot.add_cog(BirthdayCog(sbbot))
