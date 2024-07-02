import calendar
import datetime

import discord
from discord.ext import commands

from lib.embeds.info import BdayInfo
from services.birthday_service import Birthday


async def add(ctx, month, month_index, day):
    """Set a user's birthday in a specific guild."""
    leap_year = 2020
    max_days = calendar.monthrange(leap_year, month_index)[1]

    if not (1 <= day <= max_days):
        raise commands.BadArgument("the date you entered is invalid.")

    date_str = f"{leap_year}-{month_index:02d}-{day:02d}"
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")

    birthday = Birthday(ctx.author.id, ctx.guild.id)
    birthday.set(date_obj)

    await ctx.respond(embed=BdayInfo.set_month(ctx, month, day))


async def delete(ctx):
    """Delete a user's birthday in a specific server."""
    birthday = Birthday(ctx.author.id, ctx.guild.id)
    birthday.delete()
    await ctx.respond(embed=BdayInfo.delete(ctx))


async def upcoming(ctx):
    """Get the upcoming birthdays for a specific server."""
    upcoming_birthdays = Birthday.get_upcoming_birthdays(ctx.guild.id)
    icon = ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"

    embed = discord.Embed(color=discord.Color.embed_background())
    embed.set_author(name="Upcoming Birthdays!", icon_url=icon)
    embed.set_thumbnail(url="https://i.imgur.com/79XfsbS.png")

    found_birthdays = 0
    for user_id, birthday in upcoming_birthdays:
        try:
            member = await ctx.guild.fetch_member(user_id)
            name = member.name
        except discord.HTTPException:
            continue  # skip user if not in guild

        try:
            birthday_date = datetime.datetime.strptime(birthday, "%m-%d")
            formatted_birthday = birthday_date.strftime("%B %-d")
        except ValueError:
            # leap year error
            formatted_birthday = "February 29"

        embed.add_field(name=f"{name}", value=f"🎂 {formatted_birthday}", inline=False)

        found_birthdays += 1
        if found_birthdays >= 5:
            break

    await ctx.respond(embed=embed)
