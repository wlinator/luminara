from loguru import logger

from discord.ext.commands import Cog

import lib.embeds.boost
from lib.embeds.greet import Greet
from services.config_service import GuildConfig
from services.blacklist_service import BlacklistUserService


class EventHandler(Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_member_join(self, member):
        if BlacklistUserService.is_user_blacklisted(member.id):
            return

        config = GuildConfig(member.guild.id)

        if not config.welcome_channel_id:
            return

        embed = Greet.message(member, config.welcome_message)

        try:
            await member.guild.get_channel(config.welcome_channel_id).send(embed=embed, content=member.mention)
        except Exception as e:
            logger.warning(f"Greet message not sent in '{member.guild.name}'. Channel ID may be invalid. {e}")

    @Cog.listener()
    async def on_member_update(self, before, after):
        if BlacklistUserService.is_user_blacklisted(after.id):
            return

        if before.premium_since is None and after.premium_since is not None:
            await self.on_nitro_boost(after)

    @staticmethod
    async def on_nitro_boost(member):
        config = GuildConfig(member.guild.id)

        if not config.boost_channel_id:
            return

        embed = lib.embeds.boost.Boost.message(member, config.boost_message, config.boost_image_url)

        try:
            await member.guild.get_channel(config.boost_channel_id).send(embed=embed, content=member.mention)
        except Exception as e:
            logger.warning(f"Boost message not sent in '{member.guild.name}'. Channel ID may be invalid. {e}")

    @Cog.listener()
    async def on_command_completion(self, ctx) -> None:
        log_msg = '%s executed .%s' % (ctx.author.name, ctx.command.qualified_name)

        if ctx.guild is not None:
            logger.debug(f"{log_msg} | guild: {ctx.guild.name} ")
        else:
            logger.debug(f"{log_msg} in DMs")

    @Cog.listener()
    async def on_application_command_completion(self, ctx) -> None:
        log_msg = '%s executed /%s' % (ctx.author.name, ctx.command.qualified_name)

        if ctx.guild is not None:
            logger.debug(f"{log_msg} | guild: {ctx.guild.name} ")
        else:
            logger.debug(f"{log_msg} in DMs")


def setup(client):
    client.add_cog(EventHandler(client))
