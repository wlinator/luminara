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
from services.GuildConfig import GuildConfig
from main import strings
from lib import time, checks

logs = logging.getLogger('Racu.Core')
data = json_loader.load_birthday()
months = data["months"]
messages = data["birthday_messages"]


class BirthdayCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.daily_birthday_check.start()

    birthday = SlashCommandGroup("birthday", "various birthday commands.", guild_only=True)

    @birthday.command(
        name="set",
        description="Set your birthday."
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(checks.birthday_module)
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

        birthday = Birthday(ctx.author.id, ctx.guild.id)
        birthday.set(date_obj)

        await ctx.respond(strings["birthday_set"].format(ctx.author.name, month, day), ephemeral=True)

    @birthday.command(
        name="upcoming",
        description="See upcoming birthdays!"
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(checks.birthday_module)
    async def upcoming_birthdays(self, ctx):
        upcoming_birthdays = Birthday.get_upcoming_birthdays(ctx.guild.id)
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
                channel = await guild.fetch_channel(guild_config.birthday_channel_id)
                await channel.send(embed=embed, content=member.mention)
                logs.info(f"[BirthdayHandler] Success! user/guild/channel ID: {member.id}/{guild.id}/{channel.id}")

            except Exception as error:
                logs.info(f"[BirthdayHandler] Skipped processing user/guild {user_id}/{guild_id}")

            # wait one second to avoid rate limits
            await asyncio.sleep(1)


def setup(client):
    client.add_cog(BirthdayCog(client))
