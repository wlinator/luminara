import asyncio
import logging
import random

import discord
from discord.ext import commands, tasks, bridge
from discord.commands import SlashCommandGroup

from config.parser import JsonCache
from lib import time, checks
from modules.birthdays import birthday
from services.birthday_service import Birthday
from services.config_service import GuildConfig

_logs = logging.getLogger('Lumi.Core')
_data = JsonCache.read_json("birthday")
_months = _data["months"]
_messages = _data["birthday_messages"]


class Birthdays(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.daily_birthday_check.start()

    """
    birthday module - slash command only
    """
    birthday = SlashCommandGroup(name="birthday", description="Birthday commands.", guild_only=True)

    @birthday.command(name="set", description="Set your birthday in this server.")
    @checks.birthdays_enabled()
    async def set_birthday(self, ctx, month: discord.Option(choices=_months), day: int):
        index = _months.index(month) + 1
        await birthday.add(ctx, month, index, day)

    @birthday.command(name="delete", description="Delete your birthday in this server.")
    @commands.guild_only()
    async def delete_birthday(self, ctx):
        await birthday.delete(ctx)

    @birthday.command(name="upcoming", description="Shows the upcoming birthdays in this server.")
    @checks.birthdays_enabled()
    async def upcoming_birthdays(self, ctx):
        await birthday.upcoming(ctx)

    @tasks.loop(hours=23, minutes=55)
    async def daily_birthday_check(self):

        wait_time = time.seconds_until(7, 0)
        _logs.info(f"[BirthdayHandler] Waiting until 7 AM Eastern for daily check: {round(wait_time)}s")
        await asyncio.sleep(wait_time)

        embed = discord.Embed(color=discord.Color.embed_background())
        embed.set_image(url="https://media1.tenor.com/m/NXvU9jbBUGMAAAAC/fireworks.gif")

        for user_id, guild_id in Birthday.get_birthdays_today():
            try:
                guild = await self.client.fetch_guild(guild_id)
                member = await guild.fetch_member(user_id)
                guild_config = GuildConfig(guild.id)

                if not guild_config.birthday_channel_id:
                    _logs.info(f"[BirthdayHandler] Guild with ID {guild.id} skipped: no birthday channel defined.")
                    return

                message = random.choice(_messages)
                embed.description = message.format(member.name)
                channel = await self.client.get_or_fetch_channel(guild, guild_config.birthday_channel_id)
                await channel.send(embed=embed, content=member.mention)
                _logs.info(f"[BirthdayHandler] Success! user/guild/channel ID: {member.id}/{guild.id}/{channel.id}")

            except Exception as error:
                _logs.info(f"[BirthdayHandler] Skipped processing user/guild {user_id}/{guild_id}")

            # wait one second to avoid rate limits
            await asyncio.sleep(1)


def setup(client):
    client.add_cog(Birthdays(client))
