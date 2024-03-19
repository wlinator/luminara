import logging

import discord
from discord.ext import commands, bridge
from discord.commands import SlashCommandGroup
from services.GuildConfig import GuildConfig
from lib import formatter, embeds_old
from modules.config import config
import main

from main import strings

logs = logging.getLogger('Racu.Core')


class Config(commands.Cog):
    def __init__(self, client):
        self.client = client

    @bridge.bridge_command(
        name="configuration",
        aliases=["config"],
        guild_only=True
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def config_command(self, ctx):
        """
        Shows information about how Racu is configured in your server.
        Config guide: https://gitlab.com/wlinator/Racu/-/wikis/Server-Configuration
        """
        await config.cmd(ctx)

    config = SlashCommandGroup("config", "server config commands.", guild_only=True,
                               default_member_permissions=discord.Permissions(manage_channels=True))
    birthday_config = config.create_subgroup(name="birthdays")
    command_config = config.create_subgroup(name="commands")
    intro_config = config.create_subgroup(name="intros")
    welcome_config = config.create_subgroup(name="greetings")
    level_config = config.create_subgroup(name="levels")

    @birthday_config.command(
        name="channel",
        description="Set the birthday channel, this will automatically enable the module."
    )
    async def config_birthdays_channel(self, ctx, *, channel: discord.TextChannel):
        guild_config = GuildConfig(ctx.guild.id)
        guild_config.birthday_channel_id = channel.id
        guild_config.push()

        embed = discord.Embed(
            color=discord.Color.orange(),
            description=f"✅ | Birthday announcements will be sent in {channel.mention}."
        )
        guild_icon = ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        embed.set_author(name="Server Configuration", icon_url=guild_icon)

        return await ctx.respond(embed=embed)

    @birthday_config.command(
        name="disable",
        description="Disables birthday commands and announcements.",
    )
    async def config_birthdays_disable(self, ctx):
        guild_config = GuildConfig(ctx.guild.id)

        embed = discord.Embed(
            color=discord.Color.orange(),
        )
        guild_icon = ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        embed.set_author(name="Server Configuration", icon_url=guild_icon)

        if not guild_config.birthday_channel_id:
            embed.description = "👍 | The birthday module was already disabled."
            return await ctx.respond(embed=embed)

        else:
            guild_config.birthday_channel_id = None
            guild_config.push()
            embed.description = "✅ | The birthday module was successfully disabled."
            return await ctx.respond(embed=embed)

    @command_config.command(
        name="channel",
        description="If set, commands can only be done in the specified channel."
    )
    async def config_commands_channel(self, ctx, *, channel: discord.TextChannel):
        guild_config = GuildConfig(ctx.guild.id)
        guild_config.command_channel_id = channel.id
        guild_config.push()

        embed = discord.Embed(
            color=discord.Color.orange(),
            description=f"✅ | Commands can now only be used in {channel.mention}."
        )
        guild_icon = ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        embed.set_author(name="Server Configuration", icon_url=guild_icon)
        embed.set_footer(text="Note: mod & config commands are still available everywhere.")

        return await ctx.respond(embed=embed)

    @command_config.command(
        name="everywhere",
        description="Allow members to do commands in all channels."
    )
    async def config_commands_everywhere(self, ctx):
        guild_config = GuildConfig(ctx.guild.id)
        guild_config.command_channel_id = None
        guild_config.push()

        embed = discord.Embed(
            color=discord.Color.orange(),
            description=f"✅ | Server members can now use Racu commands in all channels. "
        )
        guild_icon = ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        embed.set_author(name="Server Configuration", icon_url=guild_icon)

        return await ctx.respond(embed=embed)

    @intro_config.command(
        name="channel",
        description="Set the introductions channel. This will automatically enable the module."
    )
    async def config_intros_channel(self, ctx, *, channel: discord.TextChannel):
        guild_config = GuildConfig(ctx.guild.id)
        guild_config.intro_channel_id = channel.id
        guild_config.push()

        embed = discord.Embed(
            color=discord.Color.orange(),
            description=f"✅ | New introductions will be sent in {channel.mention}."
        )
        guild_icon = ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        embed.set_author(name="Server Configuration", icon_url=guild_icon)

        return await ctx.respond(embed=embed)

    @intro_config.command(
        name="disable",
        introduction="Disable the introductions module."
    )
    async def config_intros_disable(self, ctx):
        guild_config = GuildConfig(ctx.guild.id)

        embed = discord.Embed(
            color=discord.Color.orange(),
        )
        guild_icon = ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        embed.set_author(name="Server Configuration", icon_url=guild_icon)

        if not guild_config.intro_channel_id:
            embed.description = "👍 | The introductions module was already disabled."
            return await ctx.respond(embed=embed)

        else:
            guild_config.intro_channel_id = None
            guild_config.push()
            embed.description = "✅ | The introductions module was successfully disabled."
            return await ctx.respond(embed=embed)

    @welcome_config.command(
        name="channel",
        description="Sets the welcome message channel, This will automatically enable the module."
    )
    async def config_welcome_channel(self, ctx, *, channel: discord.TextChannel):
        guild_config = GuildConfig(ctx.guild.id)
        guild_config.welcome_channel_id = channel.id
        guild_config.push()

        embed = discord.Embed(
            color=discord.Color.orange(),
            description=f"✅ | New members will receive a welcome message in {channel.mention}."
        )
        guild_icon = ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        embed.set_author(name="Server Configuration", icon_url=guild_icon)

        return await ctx.respond(embed=embed)

    @welcome_config.command(
        name="disable",
        description="Disables welcome messages in this server."
    )
    async def config_welcome_disable(self, ctx):
        guild_config = GuildConfig(ctx.guild.id)

        embed = discord.Embed(
            color=discord.Color.orange(),
        )
        guild_icon = ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        embed.set_author(name="Server Configuration", icon_url=guild_icon)

        if not guild_config.welcome_channel_id:
            embed.description = "👍 | The greeting module was already disabled."
            return await ctx.respond(embed=embed)

        else:
            guild_config.welcome_channel_id = None
            guild_config.welcome_message = None
            guild_config.push()
            embed.description = "✅ | The greeting module was successfully disabled."
            return await ctx.respond(embed=embed)

    @welcome_config.command(
        name="template",
        description="Racu will use this template text in the \"description\" field in the welcome embed."
    )
    async def config_welcome_template(self, ctx, *, text: discord.Option(str, max_length=2000)):
        guild_config = GuildConfig(ctx.guild.id)
        guild_config.welcome_message = text
        guild_config.push()

        embed = discord.Embed(
            color=discord.Color.orange(),
            description=f"✅ | The greeting template was successfully updated."
        )
        guild_icon = ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        embed.add_field(name="Template", value=text, inline=False)
        embed.add_field(name="Example", value="An example will be sent in a separate message.", inline=False)
        embed.set_author(name="Server Configuration", icon_url=guild_icon)
        await ctx.respond(embed=embed)

        embed = embeds_old.welcome_message(ctx.author, text)
        return await ctx.send(embed=embed, content=ctx.author.mention)

    @level_config.command(
        name="channel",
        description="Sets the channel for level announcements."
    )
    async def config_level_channel(self, ctx, *, channel: discord.TextChannel):
        guild_config = GuildConfig(ctx.guild.id)
        guild_config.level_channel_id = channel.id
        guild_config.push()

        embed = discord.Embed(
            color=discord.Color.orange(),
            description=f"✅ | All level announcements will be sent in {channel.mention}."
        )
        guild_icon = ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        embed.set_author(name="Server Configuration", icon_url=guild_icon)

        if guild_config.level_message_type == 0:
            embed.set_footer(text="Warning: this module is disabled, please do '/config levels enable'")

        return await ctx.respond(embed=embed)

    @level_config.command(
        name="currentchannel",
        description="Level announcements will be sent in the same channel of the message that triggers this event."
    )
    async def config_level_samechannel(self, ctx):
        guild_config = GuildConfig(ctx.guild.id)
        guild_config.level_channel_id = None
        guild_config.push()

        embed = discord.Embed(
            color=discord.Color.orange(),
            description=f"✅ | Members will receive level announcements in their current channel."
        )
        guild_icon = ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        embed.set_author(name="Server Configuration", icon_url=guild_icon)

        if guild_config.level_message_type == 0:
            embed.set_footer(text="Warning: this module is disabled, please do '/config levels enable'")

        return await ctx.respond(embed=embed)

    @level_config.command(
        name="disable",
        description="Disable levels and the Racu XP system."
    )
    async def config_level_disable(self, ctx):
        guild_config = GuildConfig(ctx.guild.id)
        guild_config.level_message_type = 0
        guild_config.push()

        embed = discord.Embed(
            color=discord.Color.orange(),
            description=f"✅ | The Racu XP system was successfully disabled."
        )
        guild_icon = ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        embed.set_author(name="Server Configuration", icon_url=guild_icon)

        return await ctx.respond(embed=embed)

    @level_config.command(
        name="enable",
        description="Enable levels and the Racu XP system."
    )
    async def config_level_enable(self, ctx):
        guild_config = GuildConfig(ctx.guild.id)

        embed = discord.Embed(
            color=discord.Color.orange(),
        )
        guild_icon = ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        embed.set_author(name="Server Configuration", icon_url=guild_icon)

        if guild_config.level_message_type != 0:
            embed.description = "👍 | The Racu XP system was already enabled."
            return await ctx.respond(embed=embed)

        else:
            guild_config.level_message_type = 1
            guild_config.push()
            embed.description = f"✅ | The Racu XP system was successfully enabled."
            embed.set_footer(text="Note: see '.help config' for more info.")
            return await ctx.respond(embed=embed)

    @level_config.command(
        name="type",
        description="Toggle level announcement types (whimsical or generic). If used, the template is removed."
    )
    async def config_level_type(self, ctx, *, type: discord.Option(choices=["whimsical", "generic"])):
        guild_config = GuildConfig(ctx.guild.id)

        embed = discord.Embed(
            color=discord.Color.orange(),
        )
        guild_icon = ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        embed.set_author(name="Server Configuration", icon_url=guild_icon)

        if type == "whimsical":
            guild_config.level_message_type = 1
            guild_config.level_message = None
            guild_config.push()

            embed.description = "✅ | Level announcements will be sarcastic comments."
            embed.add_field(name="Example", value="📈 | **lucas** Lol it took you this long to reach **Level 15**.",
                            inline=False)
            return await ctx.respond(embed=embed)

        else:
            guild_config.level_message_type = 2
            guild_config.level_message = None
            guild_config.push()

            embed.description = "✅ | Level announcements will be generic messages."
            embed.add_field(name="Example", value="📈 | **lucas** you have reached **Level 15**.", inline=False)
            return await ctx.respond(embed=embed)

    @level_config.command(
        name="template",
        description=f"If set, Racu will only use this template for level announcements. See '.help config' for info."
    )
    async def config_level_template(self, ctx, *, text: discord.Option(str, max_length=2000)):
        guild_config = GuildConfig(ctx.guild.id)
        guild_config.level_message = text
        guild_config.push()

        preview = formatter.template(text, "Lucas", 15)

        embed = discord.Embed(
            color=discord.Color.orange(),
            description=f"✅ | The level template was successfully updated."
        )
        guild_icon = ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        embed.add_field(name="Template", value=text, inline=False)
        embed.add_field(name="Example", value=preview, inline=False)
        embed.set_author(name="Server Configuration", icon_url=guild_icon)

        if guild_config.level_message_type == 0:
            embed.set_footer(text="Warning: this module is disabled, please do '/config levels enable'")

        return await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(Config(client))
