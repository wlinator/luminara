import discord
from discord import app_commands
from discord.ext import commands

from lib.const import CONST
from services.config_service import GuildConfig
from services.modlog_service import ModLogService
from ui.embeds import Builder


@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
class Config(commands.GroupCog, group_name="config"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    birthdays = app_commands.Group(name="birthdays", description="Birthday commands")
    levels = app_commands.Group(name="levels", description="Level commands")
    moderation = app_commands.Group(name="moderation", description="Moderation commands")
    prefix = app_commands.Group(name="prefix", description="Prefix commands")
    boosts = app_commands.Group(name="boosts", description="Boost commands")
    greets = app_commands.Group(name="greets", description="Greet commands")

    @app_commands.command(name="show")
    async def config_help(self, interaction: discord.Interaction) -> None:
        assert interaction.guild
        guild_config: GuildConfig = GuildConfig(interaction.guild.id)
        guild: discord.Guild = interaction.guild
        embed: discord.Embed = Builder.create_embed(
            theme="success",
            user_name=interaction.user.name,
            author_text=CONST.STRINGS["config_show_author"].format(guild.name),
            thumbnail_url=guild.icon.url if guild.icon else CONST.LUMI_LOGO_TRANSPARENT,
            hide_name_in_description=True,
        )

        config_items: list[tuple[str, bool, bool]] = [
            (
                CONST.STRINGS["config_show_birthdays"],
                bool(guild_config.birthday_channel_id),
                False,
            ),
            (
                CONST.STRINGS["config_show_new_member_greets"],
                bool(guild_config.welcome_channel_id),
                False,
            ),
            (
                CONST.STRINGS["config_show_boost_announcements"],
                bool(guild_config.boost_channel_id),
                False,
            ),
            (
                CONST.STRINGS["config_show_level_announcements"],
                guild_config.level_message_type != 0,
                False,
            ),
        ]

        for name, enabled, default_enabled in config_items:
            status: str = CONST.STRINGS["config_show_enabled"] if enabled else CONST.STRINGS["config_show_disabled"]
            if not enabled and default_enabled:
                status = CONST.STRINGS["config_show_default_enabled"]
            embed.add_field(name=name, value=status, inline=False)

        modlog_service: ModLogService = ModLogService()
        modlog_channel_id: int | None = modlog_service.fetch_modlog_channel_id(guild.id)
        modlog_channel = guild.get_channel(modlog_channel_id) if modlog_channel_id else None

        modlog_status: str
        if modlog_channel:
            modlog_status = CONST.STRINGS["config_show_moderation_log_enabled"].format(
                modlog_channel.mention,
            )
        elif modlog_channel_id:
            modlog_status = CONST.STRINGS["config_show_moderation_log_channel_deleted"]
        else:
            modlog_status = CONST.STRINGS["config_show_moderation_log_not_configured"]

            embed.add_field(
                name=CONST.STRINGS["config_show_moderation_log"],
                value=modlog_status,
                inline=False,
            )

        await interaction.response.send_message(embed=embed)

    @birthdays.command(name="channel", description="The channel to set for birthday announcements")
    async def birthday_channel(self, interaction: discord.Interaction, channel: discord.TextChannel) -> None:
        if not interaction.guild:
            return

        guild_config = GuildConfig(interaction.guild.id)
        guild_config.birthday_channel_id = channel.id
        guild_config.push()

        embed = Builder.create_embed(
            theme="success",
            user_name=interaction.user.name,
            author_text=CONST.STRINGS["config_author"],
            description=CONST.STRINGS["config_birthday_channel_set"].format(
                channel.mention,
            ),
        )

        await interaction.response.send_message(embed=embed)

    @birthdays.command(name="disable")
    async def birthday_disable(self, interaction: discord.Interaction) -> None:
        if not interaction.guild:
            return

        guild_config = GuildConfig(interaction.guild.id)

        if not guild_config.birthday_channel_id:
            embed = Builder.create_embed(
                theme="warning",
                user_name=interaction.user.name,
                author_text=CONST.STRINGS["config_author"],
                description=CONST.STRINGS["config_birthday_module_already_disabled"],
            )

        else:
            embed = Builder.create_embed(
                theme="success",
                user_name=interaction.user.name,
                author_text=CONST.STRINGS["config_author"],
                description=CONST.STRINGS["config_birthday_module_disabled"],
            )
            guild_config.birthday_channel_id = None
            guild_config.push()

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Config(bot))
