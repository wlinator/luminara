import discord
from lib.embed_builder import EmbedBuilder
from lib.constants import CONST
from services.config_service import GuildConfig
from lib.exceptions.LumiExceptions import LumiException
from lib.embeds.boost import Boost


async def set_boost_channel(ctx, channel: discord.TextChannel):
    guild_config = GuildConfig(ctx.guild.id)
    guild_config.boost_channel_id = channel.id
    guild_config.push()

    embed = EmbedBuilder().create_success_embed(
        ctx=ctx,
        author_text=CONST.STRINGS["config_author"],
        description=CONST.STRINGS["config_boost_channel_set"].format(channel.mention),
    )

    return await ctx.respond(embed=embed)


async def disable_boost_module(ctx):
    guild_config = GuildConfig(ctx.guild.id)

    if not guild_config.boost_channel_id:
        embed = EmbedBuilder().create_warning_embed(
            ctx=ctx,
            author_text=CONST.STRINGS["config_author"],
            description=CONST.STRINGS["config_boost_module_already_disabled"],
        )
    else:
        guild_config.boost_channel_id = None
        guild_config.boost_message = None
        guild_config.push()
        embed = EmbedBuilder().create_success_embed(
            ctx=ctx,
            author_text=CONST.STRINGS["config_author"],
            description=CONST.STRINGS["config_boost_module_disabled"],
        )

    return await ctx.respond(embed=embed)


async def set_boost_template(ctx, text: str):
    guild_config = GuildConfig(ctx.guild.id)
    guild_config.boost_message = text
    guild_config.push()

    embed = EmbedBuilder().create_success_embed(
        ctx=ctx,
        author_text=CONST.STRINGS["config_author"],
        description=CONST.STRINGS["config_boost_template_updated"],
        footer_text=CONST.STRINGS["config_example_next_footer"],
    )
    embed.add_field(
        name=CONST.STRINGS["config_boost_template_field"],
        value=f"```{text}```",
        inline=False,
    )

    await ctx.respond(embed=embed)

    example_embed = Boost.message(ctx.author, text, guild_config.boost_image_url)
    return await ctx.send(embed=example_embed, content=ctx.author.mention)


async def set_boost_image(ctx, image_url: str | None):
    guild_config = GuildConfig(ctx.guild.id)

    if image_url is None or image_url.lower() == "original":
        guild_config.boost_image_url = None
        guild_config.push()
        image_url = None
    elif not image_url.endswith((".jpg", ".png")):
        raise LumiException(CONST.STRINGS["error_boost_image_url_invalid"])
    elif not image_url.startswith(("http://", "https://")):
        raise LumiException(CONST.STRINGS["error_image_url_invalid"])
    else:
        guild_config.boost_image_url = image_url
        guild_config.push()

    embed = EmbedBuilder().create_success_embed(
        ctx=ctx,
        author_text=CONST.STRINGS["config_author"],
        description=CONST.STRINGS["config_boost_image_updated"],
        footer_text=CONST.STRINGS["config_example_next_footer"],
    )
    embed.add_field(
        name=CONST.STRINGS["config_boost_image_field"],
        value=image_url or CONST.STRINGS["config_boost_image_original"],
        inline=False,
    )

    await ctx.respond(embed=embed)

    example_embed = Boost.message(ctx.author, guild_config.boost_message, image_url)
    return await ctx.send(embed=example_embed, content=ctx.author.mention)
