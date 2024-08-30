import discord
from discord import app_commands
from discord.ext import commands

import lib.format
from lib.const import CONST
from lib.exceptions import LumiException
from services.config_service import GuildConfig
from services.modlog_service import ModLogService
from ui.config import create_boost_embed, create_greet_embed
from ui.embeds import Builder


@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
class Config(commands.GroupCog, group_name="config"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    birthdays = app_commands.Group(name="birthdays", description="Configure the birthdays module")
    boosts = app_commands.Group(name="boosts", description="Configure the boosts module")
    greets = app_commands.Group(name="greets", description="Configure the greets module")
    levels = app_commands.Group(name="levels", description="Configure the levels module")
    moderation = app_commands.Group(name="moderation", description="Configure the moderation module")
    prefix = app_commands.Group(name="prefix", description="Configure the prefix for the bot")

    @app_commands.command(name="show")
    async def config_help(self, interaction: discord.Interaction) -> None:
        """
        Show the current configuration for the server.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction to show the config for.
        """
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

    @birthdays.command(name="channel")
    async def birthday_channel(self, interaction: discord.Interaction, channel: discord.TextChannel) -> None:
        """
        Set the birthday channel for the server.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction to set the birthday channel for.
        channel : discord.TextChannel
            The channel to set as the birthday channel.
        """
        assert interaction.guild
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
        """
        Disable the birthday module for the server.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction to disable the birthday module for.
        """
        assert interaction.guild
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

    @levels.command(name="channel")
    async def set_level_channel(self, interaction: discord.Interaction, channel: discord.TextChannel) -> None:
        """
        Set the level-up announcement channel for the server.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction to set the level-up announcement channel for.
        channel : discord.TextChannel
            The channel to set as the level-up announcement channel.
        """
        assert interaction.guild
        guild_config = GuildConfig(interaction.guild.id)
        guild_config.level_channel_id = channel.id
        guild_config.push()

        embed = Builder.create_embed(
            theme="success",
            user_name=interaction.user.name,
            author_text=CONST.STRINGS["config_author"],
            description=CONST.STRINGS["config_level_channel_set"].format(channel.mention),
        )

        if guild_config.level_message_type == 0:
            embed.set_footer(text=CONST.STRINGS["config_level_module_disabled_warning"])

        await interaction.response.send_message(embed=embed)

    @boosts.command(name="channel")
    async def set_boost_channel(self, interaction: discord.Interaction, channel: discord.TextChannel) -> None:
        """
        Set the boost announcement channel for the server.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction to set the boost announcement channel for.
        channel : discord.TextChannel
            The channel to set as the boost announcement channel.
        """
        assert interaction.guild
        guild_config = GuildConfig(interaction.guild.id)
        guild_config.boost_channel_id = channel.id
        guild_config.push()

        embed = Builder.create_embed(
            theme="success",
            user_name=interaction.user.name,
            author_text=CONST.STRINGS["config_author"],
            description=CONST.STRINGS["config_boost_channel_set"].format(channel.mention),
        )

        await interaction.response.send_message(embed=embed)

    @boosts.command(name="disable")
    async def disable_boost_module(self, interaction: discord.Interaction) -> None:
        """
        Disable the boost module for the server.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction to disable the boost module for.
        """
        assert interaction.guild
        guild_config = GuildConfig(interaction.guild.id)

        if not guild_config.boost_channel_id:
            embed = Builder.create_embed(
                theme="warning",
                user_name=interaction.user.name,
                author_text=CONST.STRINGS["config_author"],
                description=CONST.STRINGS["config_boost_module_already_disabled"],
            )
        else:
            guild_config.boost_channel_id = None
            guild_config.boost_message = None
            guild_config.push()
            embed = Builder.create_embed(
                theme="success",
                user_name=interaction.user.name,
                author_text=CONST.STRINGS["config_author"],
                description=CONST.STRINGS["config_boost_module_disabled"],
            )

        await interaction.response.send_message(embed=embed)

    @boosts.command(name="template")
    async def set_boost_template(self, interaction: discord.Interaction, text: str) -> None:
        """
        Set the boost message template for the server.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction to set the boost message template for.
        text : str
            The template text to set for boost messages.
        """
        assert interaction.guild
        guild_config = GuildConfig(interaction.guild.id)
        guild_config.boost_message = text
        guild_config.push()

        embed = Builder.create_embed(
            theme="success",
            user_name=interaction.user.name,
            author_text=CONST.STRINGS["config_author"],
            description=CONST.STRINGS["config_boost_template_updated"],
            footer_text=CONST.STRINGS["config_example_next_footer"],
        )
        embed.add_field(
            name=CONST.STRINGS["config_boost_template_field"],
            value=f"```{text}```",
            inline=False,
        )

        await interaction.response.send_message(embed=embed)

        example_embed = await create_boost_embed(
            user_name=interaction.user.name,
            user_avatar_url=interaction.user.display_avatar.url,
            boost_count=interaction.guild.premium_subscription_count,
            template=text,
            image_url=guild_config.boost_image_url,
        )
        await interaction.followup.send(embed=example_embed, content=interaction.user.mention)

    @boosts.command(name="image")
    async def set_boost_image(self, interaction: discord.Interaction, image_url: str | None) -> None:
        """
        Set the boost message image for the server.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction to set the boost message image for.
        image_url : str | None
            The image URL to set for boost messages.
        """
        assert interaction.guild
        guild_config = GuildConfig(interaction.guild.id)

        if image_url is None or image_url.lower() == "original":
            guild_config.boost_image_url = None
            guild_config.push()
            image_url = None
        elif not image_url.endswith(tuple(CONST.ALLOWED_IMAGE_EXTENSIONS)):
            raise ValueError(CONST.STRINGS["error_boost_image_url_invalid"])
        elif not image_url.startswith(("http://", "https://")):
            raise ValueError(CONST.STRINGS["error_image_url_invalid"])
        else:
            guild_config.boost_image_url = image_url
            guild_config.push()

        embed = Builder.create_embed(
            theme="success",
            user_name=interaction.user.name,
            author_text=CONST.STRINGS["config_author"],
            description=CONST.STRINGS["config_boost_image_updated"],
            footer_text=CONST.STRINGS["config_example_next_footer"],
        )
        embed.add_field(
            name=CONST.STRINGS["config_boost_image_field"],
            value=image_url or CONST.STRINGS["config_boost_image_original"],
            inline=False,
        )

        await interaction.response.send_message(embed=embed)

        example_embed = await create_boost_embed(
            user_name=interaction.user.name,
            user_avatar_url=interaction.user.display_avatar.url,
            boost_count=interaction.guild.premium_subscription_count,
            template=guild_config.boost_message,
            image_url=image_url,
        )
        await interaction.followup.send(embed=example_embed, content=interaction.user.mention)

    @greets.command(name="channel")
    async def set_welcome_channel(self, interaction: discord.Interaction, channel: discord.TextChannel) -> None:
        """
        Set the welcome channel for the server.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction to set the welcome channel for.
        channel : discord.TextChannel
            The channel to set as the welcome channel.
        """
        assert interaction.guild
        guild_config: GuildConfig = GuildConfig(interaction.guild.id)
        guild_config.welcome_channel_id = channel.id
        guild_config.push()

        embed: discord.Embed = Builder.create_embed(
            theme="success",
            user_name=interaction.user.name,
            author_text=CONST.STRINGS["config_author"],
            description=CONST.STRINGS["config_welcome_channel_set"].format(channel.mention),
        )

        await interaction.response.send_message(embed=embed)

    @greets.command(name="disable")
    async def disable_welcome_module(self, interaction: discord.Interaction) -> None:
        """
        Disable the welcome module for the server.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction to disable the welcome module for.
        """
        assert interaction.guild
        guild_config: GuildConfig = GuildConfig(interaction.guild.id)

        if not guild_config.welcome_channel_id:
            embed: discord.Embed = Builder.create_embed(
                theme="warning",
                user_name=interaction.user.name,
                author_text=CONST.STRINGS["config_author"],
                description=CONST.STRINGS["config_welcome_module_already_disabled"],
            )
        else:
            guild_config.welcome_channel_id = None
            guild_config.welcome_message = None
            guild_config.push()
            embed: discord.Embed = Builder.create_embed(
                theme="success",
                user_name=interaction.user.name,
                author_text=CONST.STRINGS["config_author"],
                description=CONST.STRINGS["config_welcome_module_disabled"],
            )

        await interaction.response.send_message(embed=embed)

    @greets.command(name="template")
    async def set_welcome_template(self, interaction: discord.Interaction, text: str) -> None:
        """
        Set the welcome message template for the server.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction to set the welcome message template for.
        text : str
            The welcome message template.
        """
        assert interaction.guild
        guild_config: GuildConfig = GuildConfig(interaction.guild.id)
        guild_config.welcome_message = text
        guild_config.push()

        embed: discord.Embed = Builder.create_embed(
            theme="success",
            user_name=interaction.user.name,
            author_text=CONST.STRINGS["config_author"],
            description=CONST.STRINGS["config_welcome_template_updated"],
            footer_text=CONST.STRINGS["config_example_next_footer"],
        )
        embed.add_field(
            name=CONST.STRINGS["config_welcome_template_field"],
            value=f"```{text}```",
            inline=False,
        )

        await interaction.response.send_message(embed=embed)

        example_embed: discord.Embed = create_greet_embed(
            user_name=interaction.user.name,
            user_avatar_url=interaction.user.display_avatar.url,
            guild_name=interaction.guild.name,
            template=text,
        )

        await interaction.followup.send(embed=example_embed, content=interaction.user.mention)

    @levels.command(name="current_channel")
    async def set_level_current_channel(self, interaction: discord.Interaction) -> None:
        """
        Set the current channel as the level-up announcement channel for the server.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction to set the current channel as the level-up announcement channel for.
        """
        assert interaction.guild
        guild_config = GuildConfig(interaction.guild.id)
        guild_config.level_channel_id = None
        guild_config.push()

        embed = Builder.create_embed(
            theme="success",
            user_name=interaction.user.name,
            author_text=CONST.STRINGS["config_author"],
            description=CONST.STRINGS["config_level_current_channel_set"],
        )

        if guild_config.level_message_type == 0:
            embed.set_footer(text=CONST.STRINGS["config_level_module_disabled_warning"])

        await interaction.response.send_message(embed=embed)

    @levels.command(name="disable")
    async def disable_level_module(self, interaction: discord.Interaction) -> None:
        """
        Disable the level-up module for the server.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction to disable the level-up module for.
        """
        assert interaction.guild
        guild_config = GuildConfig(interaction.guild.id)
        guild_config.level_message_type = 0
        guild_config.push()

        embed = Builder.create_embed(
            theme="success",
            user_name=interaction.user.name,
            author_text=CONST.STRINGS["config_author"],
            description=CONST.STRINGS["config_level_module_disabled"],
        )

        await interaction.response.send_message(embed=embed)

    @levels.command(name="enable")
    async def enable_level_module(self, interaction: discord.Interaction) -> None:
        """
        Enable the level-up module for the server.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction to enable the level-up module for.
        """
        assert interaction.guild
        guild_config = GuildConfig(interaction.guild.id)

        if guild_config.level_message_type != 0:
            embed = Builder.create_embed(
                theme="info",
                user_name=interaction.user.name,
                author_text=CONST.STRINGS["config_author"],
                description=CONST.STRINGS["config_level_module_already_enabled"],
            )
        else:
            guild_config.level_message_type = 1
            guild_config.push()
            embed = Builder.create_embed(
                theme="success",
                user_name=interaction.user.name,
                author_text=CONST.STRINGS["config_author"],
                description=CONST.STRINGS["config_level_module_enabled"],
            )

        await interaction.response.send_message(embed=embed)

    @levels.command(name="template")
    async def set_level_template(self, interaction: discord.Interaction, text: str) -> None:
        """
        Set the template for level-up messages for the server.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction to set the template for level-up messages for.
        text : str
            The template text to set for level-up messages.
        """
        assert interaction.guild
        guild_config = GuildConfig(interaction.guild.id)
        guild_config.level_message = text
        guild_config.push()

        preview = lib.format.template(text, "Lucas", 15)

        embed = Builder.create_embed(
            theme="success",
            user_name=interaction.user.name,
            author_text=CONST.STRINGS["config_author"],
            description=CONST.STRINGS["config_level_template_updated"],
        )
        embed.add_field(
            name=CONST.STRINGS["config_level_template"],
            value=f"```{text}```",
            inline=False,
        )
        embed.add_field(
            name=CONST.STRINGS["config_level_type_example"],
            value=preview,
            inline=False,
        )

        if guild_config.level_message_type == 0:
            embed.set_footer(text=CONST.STRINGS["config_level_module_disabled_warning"])

        await interaction.response.send_message(embed=embed)

    @levels.command(name="type")
    async def set_level_type(self, interaction: discord.Interaction, level_type: str) -> None:
        """
        Set the type of level-up messages for the server.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction to set the type of level-up messages for.
        level_type : str
            The type of level-up messages to set (e.g., "whimsical" or "generic").
        """
        assert interaction.guild
        guild_config = GuildConfig(interaction.guild.id)

        embed = Builder.create_embed(
            theme="success",
            user_name=interaction.user.name,
            author_text=CONST.STRINGS["config_author"],
        )

        guild_config.level_message = None
        if level_type == "whimsical":
            guild_config.level_message_type = 1
            guild_config.push()

            embed.description = CONST.STRINGS["config_level_type_whimsical"]
            embed.add_field(
                name=CONST.STRINGS["config_level_type_example"],
                value=CONST.STRINGS["config_level_type_whimsical_example"],
                inline=False,
            )
        else:
            guild_config.level_message_type = 2
            guild_config.push()

            embed.description = CONST.STRINGS["config_level_type_generic"]
            embed.add_field(
                name=CONST.STRINGS["config_level_type_example"],
                value=CONST.STRINGS["config_level_type_generic_example"],
                inline=False,
            )

        await interaction.response.send_message(embed=embed)

    @moderation.command(name="log")
    async def set_mod_log_channel(self, interaction: discord.Interaction, channel: discord.TextChannel) -> None:
        """
        Set the moderation log channel for the server.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction to set the moderation log channel for.
        channel : discord.TextChannel
            The channel to set as the moderation log channel.
        """
        assert interaction.guild
        mod_log = ModLogService()

        info_embed = Builder.create_embed(
            theme="info",
            user_name=interaction.user.name,
            author_text=CONST.STRINGS["config_modlog_info_author"],
            description=CONST.STRINGS["config_modlog_info_description"].format(
                interaction.guild.name,
            ),
            hide_name_in_description=True,
        )
        info_embed.add_field(
            name=CONST.STRINGS["config_modlog_info_commands_name"],
            value=CONST.STRINGS["config_modlog_info_commands_value"],
            inline=False,
        )
        info_embed.add_field(
            name=CONST.STRINGS["config_modlog_info_warning_name"],
            value=CONST.STRINGS["config_modlog_info_warning_value"],
            inline=False,
        )

        try:
            await channel.send(embed=info_embed)
        except discord.errors.Forbidden as e:
            raise LumiException(CONST.STRINGS["config_modlog_permission_error"]) from e

        mod_log.set_modlog_channel(interaction.guild.id, channel.id)

        success_embed = Builder.create_embed(
            theme="success",
            user_name=interaction.user.name,
            author_text=CONST.STRINGS["config_author"],
            description=CONST.STRINGS["config_modlog_channel_set"].format(channel.mention),
        )

        await interaction.response.send_message(embed=success_embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Config(bot))
