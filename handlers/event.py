
import discord
from discord.ext import commands
from loguru import logger

from lib.client import Luminara
from services.blacklist_service import BlacklistUserService
from services.config_service import GuildConfig
from services.xp_service import XpRewardService, XpService  # Added import
from ui.config import create_boost_embed, create_greet_embed


class EventHandler(commands.Cog):
    def __init__(self, bot: Luminara):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if BlacklistUserService.is_user_blacklisted(member.id):
            return

        config = GuildConfig(member.guild.id)

        # Send welcome message if configured
        if config.welcome_channel_id:
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

        # Apply persistent level roles
        await self.apply_persistent_roles(member, config)

    async def apply_persistent_roles(self, member: discord.Member, config: GuildConfig) -> None:
        """
        Applies persistent level roles to the newly joined member based on their current XP level.

        Args:
            member (discord.Member): The member who joined.
            config (GuildConfig): The guild configuration.
        """
        
        # Initialize XP services
        xp_service = XpService(member.id, member.guild.id)
        xp_reward_service = XpRewardService(member.guild.id)

        # Fetch the user's current level
        user_level = xp_service.level

        # Retrieve all persistent rewards
        persistent_rewards = {
            level: role_info
            for level, role_info in xp_reward_service.rewards.items()
            if role_info[1]  # persistent is True
        }

        # Filter roles that the user qualifies for based on their level
        eligible_roles = [
            (level, role_id)
            for level, (role_id, _) in persistent_rewards.items()
            if user_level >= level
        ]

        # Sort roles by level ascending to assign lower roles first
        eligible_roles.sort(key=lambda x: x[0])

        # Assign each eligible role to the user
        for level, role_id in eligible_roles:
            role = member.guild.get_role(role_id)
            if role is None:
                logger.warning(
                    f"Role ID {role_id} for level {level} not found in guild '{member.guild.name}'."
                )
                continue
            try:
                await member.add_roles(role, reason="Persistent level role upon joining.")
                logger.info(
                    f"Assigned persistent role '{role.name}' to user '{member.name}'."
                )
            except (discord.Forbidden, discord.HTTPException) as e:
                logger.error(
                    f"Failed to assign role '{role.name}' (ID: {role_id}) to user '{member.name}' (ID: {member.id}): {e}"
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