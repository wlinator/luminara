import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands, bridge

from config.parser import JsonCache
from lib import formatter
from lib.embeds.boost import Boost
from lib.embeds.error import GenericErrors
from lib.embeds.greet import Greet
from modules.config import config, set_prefix, xp_reward
from services.config_service import GuildConfig

strings = JsonCache.read_json("strings")


class Config(commands.Cog):
    def __init__(self, client):
        self.client = client

    @bridge.bridge_command(
        name="configuration",
        aliases=["config"],
        description="Show your server configuration.",
        help="Shows information about how Lumi is configured in your server. "
        "[Read the guide](https://wiki.wlinator.org/serverconfig).",
        guild_only=True,
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def config_command(self, ctx):
        await config.cmd(self, ctx)

    @bridge.bridge_command(
        name="setprefix",
        aliases=["sp"],
        description="Set Lumi's prefix.",
        help="Set the prefix for Lumi in this server. The maximum length of a prefix is 25.",
        guild_only=True,
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def prefix_set_command(self, ctx, *, prefix: str):
        await set_prefix.set_cmd(ctx, prefix)

    @bridge.bridge_command(
        name="xprewards",
        aliases=["xpr"],
        description="Show your server's XP rewards list.",
        help="Read [the guide](https://wiki.wlinator.org/xprewards) before editing.",
        guild_only="True",
    )
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def xp_reward_command_show(self, ctx):
        await xp_reward.show(ctx)

    @bridge.bridge_command(
        name="addxpreward",
        aliases=["axpr"],
        description="Add a Lumi XP reward.",
        help="Add a Lumi XP reward. Read [the guide](https://wiki.wlinator.org/xprewards) before editing.",
        guild_only="True",
    )
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def xp_reward_command_add(
        self,
        ctx,
        level: int,
        role: discord.Role,
        persistent: bool = False,
    ):
        await xp_reward.add_reward(ctx, level, role.id, persistent)

    @bridge.bridge_command(
        name="removexpreward",
        aliases=["rxpr"],
        description="Remove a Lumi XP reward.",
        help="Remove a Lumi XP reward. Read [the guide](https://wiki.wlinator.org/xprewards) before editing.",
        guild_only="True",
    )
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def xp_reward_command_remove(self, ctx, level: int):
        await xp_reward.remove_reward(ctx, level)

    """
    The guild config code is a mess.
    """
    config = SlashCommandGroup(
        "config",
        "server config commands.",
        guild_only=True,
        default_member_permissions=discord.Permissions(manage_channels=True),
    )
    birthday_config = config.create_subgroup(name="birthdays")
    command_config = config.create_subgroup(name="commands")
    intro_config = config.create_subgroup(name="intros")
    welcome_config = config.create_subgroup(name="greetings")
    boost_config = config.create_subgroup(name="boosts")
    level_config = config.create_subgroup(name="levels")

    @birthday_config.command(
        name="channel",
        description="Set the birthday announcements channel.",
    )
    async def config_birthdays_channel(self, ctx, *, channel: discord.TextChannel):
        guild_config = GuildConfig(ctx.guild.id)
        guild_config.birthday_channel_id = channel.id
        guild_config.push()

        embed = discord.Embed(
            color=discord.Color.orange(),
            description=f"✅ | Birthday announcements will be sent in {channel.mention}.",
        )
        guild_icon = (
            ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        )
        embed.set_author(name="Server Configuration", icon_url=guild_icon)

        return await ctx.respond(embed=embed)

    @birthday_config.command(
        name="disable",
        description="Disable the birthday module.",
    )
    async def config_birthdays_disable(self, ctx):
        guild_config = GuildConfig(ctx.guild.id)

        embed = discord.Embed(
            color=discord.Color.orange(),
        )
        guild_icon = (
            ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        )
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
        description="Configure where members can use Lumi commands.",
    )
    async def config_commands_channel(self, ctx, *, channel: discord.TextChannel):
        guild_config = GuildConfig(ctx.guild.id)
        guild_config.command_channel_id = channel.id
        guild_config.push()

        embed = discord.Embed(
            color=discord.Color.orange(),
            description=f"✅ | Commands can now only be used in {channel.mention}.",
        )
        guild_icon = (
            ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        )
        embed.set_author(name="Server Configuration", icon_url=guild_icon)
        embed.set_footer(
            text="Note: mod & config commands are still available everywhere.",
        )

        return await ctx.respond(embed=embed)

    @command_config.command(
        name="everywhere",
        description="Allow members to do commands in all channels.",
    )
    async def config_commands_everywhere(self, ctx):
        guild_config = GuildConfig(ctx.guild.id)
        guild_config.command_channel_id = None
        guild_config.push()

        embed = discord.Embed(
            color=discord.Color.orange(),
            description="✅ | Server members can now use Lumi commands in all channels. ",
        )
        guild_icon = (
            ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        )
        embed.set_author(name="Server Configuration", icon_url=guild_icon)

        return await ctx.respond(embed=embed)

    # @intro_config.command(
    #     name="channel",
    #     description="Set the introductions channel."
    # )
    # async def config_intros_channel(self, ctx, *, channel: discord.TextChannel):
    #     guild_config = GuildConfig(ctx.guild.id)
    #     guild_config.intro_channel_id = channel.id
    #     guild_config.push()
    #
    #     embed = discord.Embed(
    #         color=discord.Color.orange(),
    #         description=f"✅ | New introductions will be sent in {channel.mention}."
    #     )
    #     guild_icon = ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
    #     embed.set_author(name="Server Configuration", icon_url=guild_icon)
    #
    #     return await ctx.respond(embed=embed)
    #
    # @intro_config.command(
    #     name="disable",
    #     introduction="Disable the introductions module."
    # )
    # async def config_intros_disable(self, ctx):
    #     guild_config = GuildConfig(ctx.guild.id)
    #
    #     embed = discord.Embed(
    #         color=discord.Color.orange(),
    #     )
    #     guild_icon = ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
    #     embed.set_author(name="Server Configuration", icon_url=guild_icon)
    #
    #     if not guild_config.intro_channel_id:
    #         embed.description = "👍 | The introductions module was already disabled."
    #         return await ctx.respond(embed=embed)
    #
    #     else:
    #         guild_config.intro_channel_id = None
    #         guild_config.push()
    #         embed.description = "✅ | The introductions module was successfully disabled."
    #         return await ctx.respond(embed=embed)

    @welcome_config.command(
        name="channel",
        description="Set the greeting announcements channel.",
    )
    async def config_welcome_channel(self, ctx, *, channel: discord.TextChannel):
        guild_config = GuildConfig(ctx.guild.id)
        guild_config.welcome_channel_id = channel.id
        guild_config.push()

        embed = discord.Embed(
            color=discord.Color.orange(),
            description=f"✅ | New members will receive a welcome message in {channel.mention}.",
        )
        guild_icon = (
            ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        )
        embed.set_author(name="Server Configuration", icon_url=guild_icon)

        return await ctx.respond(embed=embed)

    @welcome_config.command(
        name="disable",
        description="Disable greetings in this server.",
    )
    async def config_welcome_disable(self, ctx):
        guild_config = GuildConfig(ctx.guild.id)

        embed = discord.Embed(
            color=discord.Color.orange(),
        )
        guild_icon = (
            ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        )
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
        description="Make a custom greeting template.",
    )
    async def config_welcome_template(
        self,
        ctx,
        *,
        text: discord.Option(str, max_length=2000),
    ):
        guild_config = GuildConfig(ctx.guild.id)
        guild_config.welcome_message = text
        guild_config.push()

        embed = discord.Embed(
            color=discord.Color.orange(),
            description="✅ | The greeting template was successfully updated.",
        )
        guild_icon = (
            ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        )
        embed.add_field(name="Template", value=text, inline=False)
        embed.add_field(
            name="Example",
            value="An example will be sent in a separate message.",
            inline=False,
        )
        embed.set_author(name="Server Configuration", icon_url=guild_icon)
        await ctx.respond(embed=embed)

        embed = Greet.message(ctx.author, text)
        return await ctx.send(embed=embed, content=ctx.author.mention)

    @boost_config.command(
        name="channel",
        description="Set the boost announcements channel.",
    )
    async def config_boosts_channel(self, ctx, *, channel: discord.TextChannel):
        guild_config = GuildConfig(ctx.guild.id)
        guild_config.boost_channel_id = channel.id
        guild_config.push()

        embed = discord.Embed(
            color=discord.Color.orange(),
            description=f"✅ | I will announce server boosts in {channel.mention}.",
        )
        guild_icon = (
            ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        )
        embed.set_author(name="Server Configuration", icon_url=guild_icon)

        return await ctx.respond(embed=embed)

    @boost_config.command(
        name="disable",
        description="Disable boost announcements in this server.",
    )
    async def config_boosts_disable(self, ctx):
        guild_config = GuildConfig(ctx.guild.id)

        embed = discord.Embed(
            color=discord.Color.orange(),
        )
        guild_icon = (
            ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        )
        embed.set_author(name="Server Configuration", icon_url=guild_icon)

        if not guild_config.boost_channel_id:
            embed.description = "👍 | Boost announcements were already disabled."
            return await ctx.respond(embed=embed)

        else:
            guild_config.boost_channel_id = None
            guild_config.boost_message = None
            guild_config.push()
            embed.description = "✅ | Boost announcements are successfully disabled."
            return await ctx.respond(embed=embed)

    @boost_config.command(
        name="template",
        description="Make a custom boost announcement template.",
    )
    async def config_boosts_template(
        self,
        ctx,
        *,
        text: discord.Option(str, max_length=2000),
    ):
        guild_config = GuildConfig(ctx.guild.id)
        guild_config.boost_message = text
        guild_config.push()

        embed = discord.Embed(
            color=discord.Color.orange(),
            description="✅ | The booster template was successfully updated.",
        )
        guild_icon = (
            ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        )
        embed.add_field(name="Template", value=text, inline=False)
        embed.add_field(
            name="Example",
            value="An example will be sent in a separate message.",
            inline=False,
        )
        embed.set_author(name="Server Configuration", icon_url=guild_icon)
        await ctx.respond(embed=embed)

        embed = Boost.message(ctx.author, text, guild_config.boost_image_url)
        return await ctx.send(embed=embed, content=ctx.author.mention)

    @boost_config.command(
        name="image",
        description="Add a custom image that will used for booster announcements.",
    )
    async def config_boosts_image(self, ctx, *, image_url: str):
        guild_config = GuildConfig(ctx.guild.id)

        if image_url.lower() == "original":
            guild_config.boost_image_url = None
            guild_config.push()
            image_url = None

        elif not image_url.endswith(".jpg") and not image_url.lower().endswith(".png"):
            return await ctx.respond(embed=GenericErrors.bad_url(ctx))

        elif not image_url.startswith("http://") and not image_url.startswith(
            "https://",
        ):
            return await ctx.respond(embed=GenericErrors.bad_url(ctx, "invalid URL."))

        else:
            guild_config.boost_image_url = image_url
            guild_config.push()

        embed = discord.Embed(
            color=discord.Color.orange(),
            description="✅ | The booster image was successfully updated.",
        )
        guild_icon = (
            ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        )
        embed.add_field(
            name="Image",
            value=image_url if image_url else "Original Image",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value="An example will be sent in a separate message.",
            inline=False,
        )
        embed.set_author(name="Server Configuration", icon_url=guild_icon)
        await ctx.respond(embed=embed)

        embed = Boost.message(ctx.author, guild_config.boost_message, image_url)
        return await ctx.send(embed=embed, content=ctx.author.mention)

    @level_config.command(
        name="channel",
        description="Set the level announcements channel.",
    )
    async def config_level_channel(self, ctx, *, channel: discord.TextChannel):
        guild_config = GuildConfig(ctx.guild.id)
        guild_config.level_channel_id = channel.id
        guild_config.push()

        embed = discord.Embed(
            color=discord.Color.orange(),
            description=f"✅ | All level announcements will be sent in {channel.mention}.",
        )
        guild_icon = (
            ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        )
        embed.set_author(name="Server Configuration", icon_url=guild_icon)

        if guild_config.level_message_type == 0:
            embed.set_footer(
                text="Warning: this module is disabled, please do '/config levels enable'",
            )

        return await ctx.respond(embed=embed)

    @level_config.command(
        name="currentchannel",
        description="Send level announcements in the member's current channel.",
    )
    async def config_level_samechannel(self, ctx):
        guild_config = GuildConfig(ctx.guild.id)
        guild_config.level_channel_id = None
        guild_config.push()

        embed = discord.Embed(
            color=discord.Color.orange(),
            description="✅ | Members will receive level announcements in their current channel.",
        )
        guild_icon = (
            ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        )
        embed.set_author(name="Server Configuration", icon_url=guild_icon)

        if guild_config.level_message_type == 0:
            embed.set_footer(
                text="Warning: this module is disabled, please do '/config levels enable'",
            )

        return await ctx.respond(embed=embed)

    @level_config.command(
        name="disable",
        description="Disable levels and the Lumi XP system.",
    )
    async def config_level_disable(self, ctx):
        guild_config = GuildConfig(ctx.guild.id)
        guild_config.level_message_type = 0
        guild_config.push()

        embed = discord.Embed(
            color=discord.Color.orange(),
            description="✅ | The Lumi XP system was successfully disabled.",
        )
        guild_icon = (
            ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        )
        embed.set_author(name="Server Configuration", icon_url=guild_icon)

        return await ctx.respond(embed=embed)

    @level_config.command(
        name="enable",
        description="Enable levels and the Lumi XP system.",
    )
    async def config_level_enable(self, ctx):
        guild_config = GuildConfig(ctx.guild.id)

        embed = discord.Embed(
            color=discord.Color.orange(),
        )
        guild_icon = (
            ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        )
        embed.set_author(name="Server Configuration", icon_url=guild_icon)

        if guild_config.level_message_type != 0:
            embed.description = "👍 | The Lumi XP system was already enabled."
            return await ctx.respond(embed=embed)

        else:
            guild_config.level_message_type = 1
            guild_config.push()
            embed.description = "✅ | The Lumi XP system was successfully enabled."
            embed.set_footer(text="Note: see '.help config' for more info.")
            return await ctx.respond(embed=embed)

    @level_config.command(
        name="type",
        description="Set the level announcements type.",
    )
    async def config_level_type(
        self,
        ctx,
        *,
        type: discord.Option(choices=["whimsical", "generic"]),
    ):
        guild_config = GuildConfig(ctx.guild.id)

        embed = discord.Embed(
            color=discord.Color.orange(),
        )
        guild_icon = (
            ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        )
        embed.set_author(name="Server Configuration", icon_url=guild_icon)

        if type == "whimsical":
            guild_config.level_message_type = 1
            guild_config.level_message = None
            guild_config.push()

            embed.description = "✅ | Level announcements will be sarcastic comments."
            embed.add_field(
                name="Example",
                value="📈 | **lucas** Lol it took you this long to reach **Level 15**.",
                inline=False,
            )
            return await ctx.respond(embed=embed)

        else:
            guild_config.level_message_type = 2
            guild_config.level_message = None
            guild_config.push()

            embed.description = "✅ | Level announcements will be generic messages."
            embed.add_field(
                name="Example",
                value="📈 | **lucas** you have reached **Level 15**.",
                inline=False,
            )
            return await ctx.respond(embed=embed)

    @level_config.command(
        name="template",
        description="Make a custom leveling template.",
    )
    async def config_level_template(
        self,
        ctx,
        *,
        text: discord.Option(str, max_length=2000),
    ):
        guild_config = GuildConfig(ctx.guild.id)
        guild_config.level_message = text
        guild_config.push()

        preview = formatter.template(text, "Lucas", 15)

        embed = discord.Embed(
            color=discord.Color.orange(),
            description="✅ | The level template was successfully updated.",
        )
        guild_icon = (
            ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        )
        embed.add_field(name="Template", value=text, inline=False)
        embed.add_field(name="Example", value=preview, inline=False)
        embed.set_author(name="Server Configuration", icon_url=guild_icon)

        if guild_config.level_message_type == 0:
            embed.set_footer(
                text="Warning: this module is disabled, please do '/config levels enable'",
            )

        return await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(Config(client))
