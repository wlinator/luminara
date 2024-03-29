import calendar
import datetime

from discord.ext import commands

from lib.embeds.error import BdayErrors
from lib.embeds.info import BdayInfo
from services.Birthday import Birthday


async def cmd(ctx, month, month_index, day):

    leap_year = 2020
    max_days = calendar.monthrange(leap_year, month_index)[1]

    if not (1 <= day <= max_days):
        raise commands.BadArgument("the date you entered is invalid.")

    date_str = f"{leap_year}-{month_index:02d}-{day:02d}"
    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')

    birthday = Birthday(ctx.author.id, ctx.guild.id)
    birthday.set(date_obj)

    await ctx.respond(embed=BdayInfo.set_month(ctx, month, day))


async def get_month_name(string, mapping):
    string = string.lower()

    for month in mapping:
        if string.startswith(month):
            return mapping[month]

    raise commands.BadArgument("I couldn't recognize that month.")


async def get_month_index(string, mapping):
    values = list(mapping.values())
    return values.index(string) + 1
