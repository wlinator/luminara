import calendar
import datetime
import logging

import discord
from discord.ext import commands

from data.Birthday import Birthday
from main import strings

racu_logs = logging.getLogger('Racu.Core')

months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]


class BirthdayCog(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot

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

    def daily_birthday_check(self):
        # check if someone's birthday is today
        pass


def setup(sbbot):
    sbbot.add_cog(BirthdayCog(sbbot))
