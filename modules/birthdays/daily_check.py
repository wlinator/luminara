import asyncio
import random
from loguru import logger
from lib.constants import CONST
from services.birthday_service import Birthday
from services.config_service import GuildConfig
from lib.embed_builder import EmbedBuilder


async def daily_birthday_check(client):
    logger.info(CONST.STRINGS["birthday_check_started"])
    birthdays_today = Birthday.get_birthdays_today()
    processed_birthdays = 0
    failed_birthdays = 0

    if birthdays_today:
        for user_id, guild_id in birthdays_today:
            try:
                guild = await client.fetch_guild(guild_id)
                member = await guild.fetch_member(user_id)
                guild_config = GuildConfig(guild.id)

                if not guild_config.birthday_channel_id:
                    logger.debug(
                        CONST.STRINGS["birthday_check_skipped"].format(guild.id),
                    )
                    continue

                message = random.choice(CONST.BIRTHDAY_MESSAGES)
                embed = EmbedBuilder.create_success_embed(
                    None,
                    author_text="Happy Birthday!",
                    description=message.format(member.name),
                    show_name=False,
                )
                embed.set_image(url=CONST.BIRTHDAY_GIF_URL)

                channel = await guild.fetch_channel(guild_config.birthday_channel_id)
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
