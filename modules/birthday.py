import asyncio
import calendar
import datetime
import logging
import random

import discord
from discord import default_permissions
from discord.commands import SlashCommandGroup
from discord.ext import commands, tasks

from config import json_loader
from services.Birthday import Birthday
from main import strings
from lib import time

logs = logging.getLogger('Racu.Core')

months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

messages = json_loader.load_birthday_messages()


class BirthdayCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.daily_birthday_check.start()

    birthday = SlashCommandGroup("birthday", "various birthday commands.")

    @birthday.command(
        name="set",
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

    @birthday.command(
        name="upcoming",
        description="See upcoming birthdays!",
        guild_only=True
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def upcoming_birthdays(self, ctx):
        upcoming_birthdays = Birthday.get_upcoming_birthdays()
        icon = ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"

        embed = discord.Embed(
            color=discord.Color.embed_background()
        )
        embed.set_author(name="Upcoming Birthdays!", icon_url=icon)
        embed.set_thumbnail(url="https://i.imgur.com/79XfsbS.png")

        for i, (user_id, birthday) in enumerate(upcoming_birthdays, start=1):
            try:
                member = await ctx.guild.fetch_member(user_id)
                name = member.name
            except:
                name = "Unknown User"

            try:
                birthday_date = datetime.datetime.strptime(birthday, "%m-%d")
                formatted_birthday = birthday_date.strftime("%B %-d")
            except ValueError:
                # leap year error
                formatted_birthday = "February 29"

            embed.add_field(
                name=f"{name}",
                value=f"🎂 {formatted_birthday}",
                inline=False
            )

        await ctx.respond(embed=embed)

    @birthday.command(
        name="override",
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
        logs.info(f"[BirthdayHandler] Waiting until 7 AM Eastern for daily check: {round(wait_time)}s")
        await asyncio.sleep(wait_time)

        birthday_ids = Birthday.today()

        if birthday_ids:
            guild_id = 719227135151046699  # Kaiju's Rave Cave
            channel_id = 741021558172287099  # Birthdays channel

            guild = await self.client.fetch_guild(guild_id)
            channel = await guild.fetch_channel(channel_id)

            for user_id in birthday_ids:

                try:
                    user = await guild.fetch_member(user_id)
                    print(user)

                    message = random.choice(messages["birthday_messages"])
                    await channel.send(message.format(user.mention))

                    logs.info(f"[BirthdayHandler] Sent message for user with ID {user_id}")

                except discord.HTTPException:
                    logs.info(f"[BirthdayHandler] Not sent because user with ID {user_id} not in Guild.")

                except Exception as err:
                    logs.error(f"[BirthdayHandler] Something went wrong: {err}")

        else:
            logs.info("[BirthdayHandler] No Birthdays Today.")


def setup(client):
    client.add_cog(BirthdayCog(client))
