import discord
from lib.embed_builder import EmbedBuilder
from lib.constants import CONST
from services.config_service import GuildConfig
from lib import formatter


async def set_level_channel(ctx, channel: discord.TextChannel):
    guild_config = GuildConfig(ctx.guild.id)
    guild_config.level_channel_id = channel.id
    guild_config.push()

    embed = EmbedBuilder().create_success_embed(
        ctx=ctx,
        author_text=CONST.STRINGS["config_author"],
        description=CONST.STRINGS["config_level_channel_set"].format(channel.mention),
    )

    if guild_config.level_message_type == 0:
        embed.set_footer(text=CONST.STRINGS["config_level_module_disabled_warning"])

    return await ctx.respond(embed=embed)


async def set_level_current_channel(ctx):
    guild_config = GuildConfig(ctx.guild.id)
    guild_config.level_channel_id = None
    guild_config.push()

    embed = EmbedBuilder().create_success_embed(
        ctx=ctx,
        author_text=CONST.STRINGS["config_author"],
        description=CONST.STRINGS["config_level_current_channel_set"],
    )

    if guild_config.level_message_type == 0:
        embed.set_footer(text=CONST.STRINGS["config_level_module_disabled_warning"])

    return await ctx.respond(embed=embed)


async def disable_level_module(ctx):
    guild_config = GuildConfig(ctx.guild.id)
    guild_config.level_message_type = 0
    guild_config.push()

    embed = EmbedBuilder().create_success_embed(
        ctx=ctx,
        author_text=CONST.STRINGS["config_author"],
        description=CONST.STRINGS["config_level_module_disabled"],
    )

    return await ctx.respond(embed=embed)


async def enable_level_module(ctx):
    guild_config = GuildConfig(ctx.guild.id)

    if guild_config.level_message_type != 0:
        embed = EmbedBuilder().create_info_embed(
            ctx=ctx,
            author_text=CONST.STRINGS["config_author"],
            description=CONST.STRINGS["config_level_module_already_enabled"],
        )
    else:
        guild_config.level_message_type = 1
        guild_config.push()
        embed = EmbedBuilder().create_success_embed(
            ctx=ctx,
            author_text=CONST.STRINGS["config_author"],
            description=CONST.STRINGS["config_level_module_enabled"],
        )

    return await ctx.respond(embed=embed)


async def set_level_type(ctx, type: str):
    guild_config = GuildConfig(ctx.guild.id)

    embed = EmbedBuilder().create_success_embed(
        ctx=ctx,
        author_text=CONST.STRINGS["config_author"],
    )

    guild_config.level_message = None
    if type == "whimsical":
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

    return await ctx.respond(embed=embed)


async def set_level_template(ctx, text: str):
    guild_config = GuildConfig(ctx.guild.id)
    guild_config.level_message = text
    guild_config.push()

    preview = formatter.template(text, "Lucas", 15)

    embed = EmbedBuilder().create_success_embed(
        ctx=ctx,
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

    return await ctx.respond(embed=embed)
