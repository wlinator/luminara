import asyncio
import random

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands, tasks
from loguru import logger

from lib import checks, time
from lib.constants import CONST
from modules.birthdays import birthday
from services.birthday_service import Birthday
from services.config_service import GuildConfig


class Birthdays(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.daily_birthday_check.start()

    """
    birthday module - slash command only
    """
    birthday = SlashCommandGroup(
        name="birthday",
        description="Birthday commands.",
        guild_only=True,
    )

    @birthday.command(name="set", description="Set your birthday in this server.")
    @checks.birthdays_enabled()
    async def set_birthday(
        self,
        ctx,
        month: discord.Option(choices=CONST.BIRTHDAY_MONTHS),
        day: int,
    ):
        index = CONST.BIRTHDAY_MONTHS.index(month) + 1
        await birthday.add(ctx, month, index, day)

    @birthday.command(name="delete", description="Delete your birthday in this server.")
    @commands.guild_only()
    async def delete_birthday(self, ctx):
        await birthday.delete(ctx)

    @birthday.command(
        name="upcoming",
        description="Shows the upcoming birthdays in this server.",
    )
    @checks.birthdays_enabled()
    async def upcoming_birthdays(self, ctx):
        await birthday.upcoming(ctx)

    @tasks.loop(hours=23, minutes=55)
    async def daily_birthday_check(self):
        wait_time = time.seconds_until(7, 0)
        logger.debug(
            f"Waiting until 7 AM Eastern for the daily birthday check: {round(wait_time)}s left.",
        )
        await asyncio.sleep(wait_time)

        embed = discord.Embed(color=discord.Color.embed_background())
        embed.set_image(url="https://media1.tenor.com/m/NXvU9jbBUGMAAAAC/fireworks.gif")

        for user_id, guild_id in Birthday.get_birthdays_today():
            try:
                guild = await self.client.fetch_guild(guild_id)
                member = await guild.fetch_member(user_id)
                guild_config = GuildConfig(guild.id)

                if not guild_config.birthday_channel_id:
                    logger.debug(
                        f"Birthday announcements in guild with ID {guild.id} skipped: no birthday channel.",
                    )
                    return

                message = random.choice(CONST.BIRTHDAY_MESSAGES)
                embed.description = message.format(member.name)
                channel = await self.client.get_or_fetch_channel(
                    guild,
                    guild_config.birthday_channel_id,
                )
                await channel.send(embed=embed, content=member.mention)
                logger.debug(
                    f"Birthday announcement Success! user/guild/chan ID: {member.id}/{guild.id}/{channel.id}",
                )

            except Exception as e:
                logger.warning(
                    f"Birthday announcement skipped processing user/guild {user_id}/{guild_id} | {e}",
                )

            # wait one second to avoid rate limits
            await asyncio.sleep(1)


def setup(client):
    client.add_cog(Birthdays(client))
