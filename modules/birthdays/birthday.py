import datetime
import calendar

from services.Birthday import Birthday
from lib.embeds.error import BdayErrors

from main import strings


async def cmd(ctx, month, month_index, day):

    leap_year = 2020
    max_days = calendar.monthrange(leap_year, month_index)[1]

    if not (1 <= day <= max_days):
        return await ctx.respond(embed=BdayErrors.invalid_date(ctx))

    date_str = f"{leap_year}-{month_index:02d}-{day:02d}"
    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')

    birthday = Birthday(ctx.author.id, ctx.guild.id)
    birthday.set(date_obj)

    await ctx.respond(strings["birthday_set"].format(ctx.author.name, month, day), ephemeral=True)