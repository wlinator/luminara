import calendar
import datetime

import discord
from discord.ext import commands

from lib.constants import CONST
from lib.embed_builder import EmbedBuilder
from services.birthday_service import Birthday


async def add(ctx, month, month_index, day):
    leap_year = 2020
    max_days = calendar.monthrange(leap_year, month_index)[1]

    if not 1 <= day <= max_days:
        raise commands.BadArgument(CONST.STRINGS["birthday_add_invalid_date"])

    date_obj = datetime.datetime(leap_year, month_index, day)

    birthday = Birthday(ctx.author.id, ctx.guild.id)
    birthday.set(date_obj)

    embed = EmbedBuilder.create_success_embed(
        ctx,
        author_text=CONST.STRINGS["birthday_add_success_author"],
        description=CONST.STRINGS["birthday_add_success_description"].format(
            month,
            day,
        ),
        show_name=True,
    )
    await ctx.respond(embed=embed)


async def delete(ctx):
    Birthday(ctx.author.id, ctx.guild.id).delete()

    embed = EmbedBuilder.create_success_embed(
        ctx,
        author_text=CONST.STRINGS["birthday_delete_success_author"],
        description=CONST.STRINGS["birthday_delete_success_description"],
        show_name=True,
    )
    await ctx.respond(embed=embed)


async def upcoming(ctx):
    upcoming_birthdays = Birthday.get_upcoming_birthdays(ctx.guild.id)

    if not upcoming_birthdays:
        embed = EmbedBuilder.create_warning_embed(
            ctx,
            author_text=CONST.STRINGS["birthday_upcoming_no_birthdays_author"],
            description=CONST.STRINGS["birthday_upcoming_no_birthdays"],
            show_name=True,
        )
        await ctx.respond(embed=embed)
        return

    embed = EmbedBuilder.create_success_embed(
        ctx,
        author_text=CONST.STRINGS["birthday_upcoming_author"],
        description="",
        show_name=False,
    )
    embed.set_thumbnail(url=CONST.LUMI_LOGO_TRANSPARENT)

    birthday_lines = []
    for user_id, birthday in upcoming_birthdays[:10]:
        try:
            member = await ctx.guild.fetch_member(user_id)
            birthday_date = datetime.datetime.strptime(birthday, "%m-%d")
            formatted_birthday = birthday_date.strftime("%B %-d")
            birthday_lines.append(
                CONST.STRINGS["birthday_upcoming_description_line"].format(
                    member.name,
                    formatted_birthday,
                ),
            )
        except (discord.HTTPException, ValueError):
            continue

    embed.description = "\n".join(birthday_lines)
    await ctx.respond(embed=embed)
