import discord
from discord import app_commands
from discord.ext import commands

from lib.const import CONST
from services.config_service import GuildConfig
from ui.embeds import Builder


class BirthdayConfig(commands.GroupCog, group_name="config"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    birthday = app_commands.Group(name="birthday", description="Birthday commands")

    @birthday.command(name="channel", description="Set the birthday announcement channel")
    @app_commands.describe(channel="The channel to set for birthday announcements")
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

    @birthday.command(name="disable", description="Disable the birthday module")
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
    await bot.add_cog(BirthdayConfig(bot))
