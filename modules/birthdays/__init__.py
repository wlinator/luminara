import datetime

import discord
import pytz
from discord.commands import SlashCommandGroup
from discord.ext import commands, tasks

from lib import checks
from lib.constants import CONST
from modules.birthdays import birthday, daily_check


class Birthdays(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.daily_birthday_check.start()

    birthday = SlashCommandGroup(
        name="birthday",
        description="Birthday commands.",
        contexts={discord.InteractionContextType.guild},
    )

    @birthday.command(name="set", description="Set your birthday in this server.")
    @checks.birthdays_enabled()
    @discord.commands.option(name="month", choices=CONST.BIRTHDAY_MONTHS)
    async def set_birthday(self, ctx, month, day: int):
        index = CONST.BIRTHDAY_MONTHS.index(month) + 1
        await birthday.add(ctx, month, index, day)

    @birthday.command(name="delete", description="Delete your birthday in this server.")
    async def delete_birthday(self, ctx):
        await birthday.delete(ctx)

    @birthday.command(name="upcoming", description="Shows the upcoming birthdays.")
    @checks.birthdays_enabled()
    async def upcoming_birthdays(self, ctx):
        await birthday.upcoming(ctx)

    @tasks.loop(time=datetime.time(hour=12, minute=0, tzinfo=pytz.UTC))  # 12 PM UTC
    async def daily_birthday_check(self):
        await daily_check.daily_birthday_check(self.client)


def setup(client):
    client.add_cog(Birthdays(client))
