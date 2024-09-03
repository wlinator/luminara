import discord
from discord.ext import commands
from loguru import logger

from lib.client import Luminara
from services.blacklist_service import BlacklistUserService
from services.config_service import GuildConfig
from ui.config import create_boost_embed, create_greet_embed


class EventHandler(commands.Cog):
    def __init__(self, bot: Luminara):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if BlacklistUserService.is_user_blacklisted(member.id):
            return

        config = GuildConfig(member.guild.id)

        if not config.welcome_channel_id:
            return

        embed = create_greet_embed(
            user_name=member.name,
            user_avatar_url=member.display_avatar.url,
            guild_name=member.guild.name,
            template=config.welcome_message,
        )

        try:
            channel = member.guild.get_channel(config.welcome_channel_id)
            if isinstance(channel, discord.TextChannel):
                await channel.send(
                    embed=embed,
                    content=member.mention,
                )
        except Exception as e:
            logger.warning(
                f"Greet message not sent in '{member.guild.name}'. Channel ID may be invalid. {e}",
            )

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if BlacklistUserService.is_user_blacklisted(after.id):
            return

        if before.premium_since is None and after.premium_since is not None:
            await self.on_nitro_boost(after)

    @staticmethod
    async def on_nitro_boost(member: discord.Member):
        config = GuildConfig(member.guild.id)

        if not config.boost_channel_id:
            return

        embed = create_boost_embed(
            user_name=member.name,
            user_avatar_url=member.display_avatar.url,
            boost_count=member.guild.premium_subscription_count,
            template=config.boost_message,
            image_url=config.boost_image_url,
        )

        try:
            channel = member.guild.get_channel(config.boost_channel_id)
            if isinstance(channel, discord.TextChannel):
                await channel.send(
                    embed=embed,
                    content=member.mention,
                )
        except Exception as e:
            logger.warning(
                f"Boost message not sent in '{member.guild.name}'. Channel ID may be invalid. {e}",
            )

    @commands.Cog.listener()
    async def on_command_completion(self, ctx: commands.Context[Luminara]) -> None:
        log_msg = f"{ctx.author.name} executed .{ctx.command.qualified_name if ctx.command else 'Unknown'}"

        if ctx.guild is not None:
            logger.debug(f"{log_msg} | guild: {ctx.guild.name} ")
        else:
            logger.debug(f"{log_msg} in DMs")

    @commands.Cog.listener()
    async def on_application_command_completion(self, ctx: discord.Interaction) -> None:
        log_msg = f"{ctx.user.name} executed /{ctx.command.qualified_name if ctx.command else 'Unknown'}"

        if ctx.guild is not None:
            logger.debug(f"{log_msg} | guild: {ctx.guild.name} ")
        else:
            logger.debug(f"{log_msg} in DMs")


async def setup(bot: Luminara):
    await bot.add_cog(EventHandler(bot))
