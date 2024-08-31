import asyncio
import calendar
import datetime
import random

import discord
import pytz
from discord import app_commands
from discord.ext import commands, tasks
from loguru import logger

from lib.checks import birthdays_enabled
from lib.const import CONST
from services.birthday_service import BirthdayService
from services.config_service import GuildConfig
from ui.embeds import Builder

tz = pytz.timezone("America/New_York")


@app_commands.guild_only()
@app_commands.default_permissions(manage_guild=True)
class Birthday(commands.GroupCog, group_name="birthday"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.daily_birthday_check.start()

    @tasks.loop(time=datetime.time(hour=12, minute=0, tzinfo=pytz.UTC))
    async def daily_birthday_check(self):
        logger.info(CONST.STRINGS["birthday_check_started"])
        birthdays_today = BirthdayService.get_birthdays_today()
        processed_birthdays = 0
        failed_birthdays = 0

        if birthdays_today:
            for user_id, guild_id in birthdays_today:
                try:
                    guild = await self.bot.fetch_guild(guild_id)
                    member = await guild.fetch_member(user_id)
                    guild_config = GuildConfig(guild.id)

                    if not guild_config.birthday_channel_id:
                        logger.debug(
                            CONST.STRINGS["birthday_check_skipped"].format(guild.id),
                        )
                        continue

                    message = random.choice(CONST.BIRTHDAY_MESSAGES)
                    embed = Builder.create_embed(
                        theme="success",
                        author_text="Happy Birthday!",
                        description=message.format(member.name),
                        hide_name_in_description=True,
                    )
                    embed.set_image(url=CONST.BIRTHDAY_GIF_URL)

                    channel = await guild.fetch_channel(guild_config.birthday_channel_id)
                    assert isinstance(channel, discord.TextChannel)
                    await channel.send(embed=embed, content=member.mention)
                    logger.debug(
                        CONST.STRINGS["birthday_check_success"].format(
                            member.id,
                            guild.id,
                            channel.id,
                        ),
                    )
                    processed_birthdays += 1

                except Exception as e:
                    logger.warning(
                        CONST.STRINGS["birthday_check_error"].format(user_id, guild_id, e),
                    )
                    failed_birthdays += 1

                # wait one second to avoid rate limits
                await asyncio.sleep(1)

        logger.info(
            CONST.STRINGS["birthday_check_finished"].format(
                processed_birthdays,
                failed_birthdays,
            ),
        )

    @app_commands.command(name="set")
    @birthdays_enabled()
    @app_commands.choices(
        month=[discord.app_commands.Choice(name=month_name, value=month_name) for month_name in CONST.BIRTHDAY_MONTHS],
    )
    async def set_birthday(
        self,
        interaction: discord.Interaction,
        month: str,
        day: int,
    ) -> None:
        """
        Set your birthday.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction object.
        month : Month
            The month of your birthday.
        day : int
            The day of your birthday.
        """
        assert interaction.guild
        leap_year = 2020
        month_index = CONST.BIRTHDAY_MONTHS.index(month) + 1
        max_days = calendar.monthrange(leap_year, month_index)[1]

        if not 1 <= day <= max_days:
            raise commands.BadArgument(CONST.STRINGS["birthday_add_invalid_date"])

        date_obj = datetime.datetime(leap_year, month_index, day, tzinfo=tz)

        birthday = BirthdayService(interaction.user.id, interaction.guild.id)
        birthday.set(date_obj)

        embed = Builder.create_embed(
            theme="success",
            user_name=interaction.user.name,
            author_text=CONST.STRINGS["birthday_add_success_author"],
            description=CONST.STRINGS["birthday_add_success_description"].format(
                month,
                day,
            ),
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="remove")
    async def remove_birthday(
        self,
        interaction: discord.Interaction,
    ) -> None:
        """
        Remove your birthday.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction object.
        """
        assert interaction.guild
        BirthdayService(interaction.user.id, interaction.guild.id).delete()

        embed = Builder.create_embed(
            theme="success",
            user_name=interaction.user.name,
            author_text=CONST.STRINGS["birthday_delete_success_author"],
            description=CONST.STRINGS["birthday_delete_success_description"],
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="upcoming")
    @birthdays_enabled()
    async def upcoming_birthdays(
        self,
        interaction: discord.Interaction,
    ) -> None:
        """
        View upcoming birthdays.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction object.
        """
        assert interaction.guild
        upcoming_birthdays = BirthdayService.get_upcoming_birthdays(interaction.guild.id)

        if not upcoming_birthdays:
            embed = Builder.create_embed(
                theme="warning",
                user_name=interaction.user.name,
                author_text=CONST.STRINGS["birthday_upcoming_no_birthdays_author"],
                description=CONST.STRINGS["birthday_upcoming_no_birthdays"],
            )
            await interaction.response.send_message(embed=embed)
            return

        embed = Builder.create_embed(
            theme="success",
            user_name=interaction.user.name,
            author_text=CONST.STRINGS["birthday_upcoming_author"],
            description="",
        )
        embed.set_thumbnail(url=CONST.LUMI_LOGO_TRANSPARENT)

        birthday_lines: list[str] = []
        for user_id, birthday in upcoming_birthdays[:10]:
            try:
                member = await interaction.guild.fetch_member(user_id)
                birthday_date = datetime.datetime.strptime(birthday, "%m-%d").replace(tzinfo=tz)
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
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Birthday(bot))
