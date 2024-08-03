import discord
from lib.embed_builder import EmbedBuilder
from lib.constants import CONST
from services.config_service import GuildConfig
from lib.embeds.greet import Greet


async def set_welcome_channel(ctx, channel: discord.TextChannel):
    guild_config = GuildConfig(ctx.guild.id)
    guild_config.welcome_channel_id = channel.id
    guild_config.push()

    embed = EmbedBuilder().create_success_embed(
        ctx=ctx,
        author_text=CONST.STRINGS["config_author"],
        description=CONST.STRINGS["config_welcome_channel_set"].format(channel.mention),
    )

    return await ctx.respond(embed=embed)


async def disable_welcome_module(ctx):
    guild_config = GuildConfig(ctx.guild.id)

    if not guild_config.welcome_channel_id:
        embed = EmbedBuilder().create_warning_embed(
            ctx=ctx,
            author_text=CONST.STRINGS["config_author"],
            description=CONST.STRINGS["config_welcome_module_already_disabled"],
        )
    else:
        guild_config.welcome_channel_id = None
        guild_config.welcome_message = None
        guild_config.push()
        embed = EmbedBuilder().create_success_embed(
            ctx=ctx,
            author_text=CONST.STRINGS["config_author"],
            description=CONST.STRINGS["config_welcome_module_disabled"],
        )

    return await ctx.respond(embed=embed)


async def set_welcome_template(ctx, text: str):
    guild_config = GuildConfig(ctx.guild.id)
    guild_config.welcome_message = text
    guild_config.push()

    embed = EmbedBuilder().create_success_embed(
        ctx=ctx,
        author_text=CONST.STRINGS["config_author"],
        description=CONST.STRINGS["config_welcome_template_updated"],
        footer_text=CONST.STRINGS["config_welcome_template_updated_footer"],
    )
    embed.add_field(
        name=CONST.STRINGS["config_welcome_template_field"],
        value=f"```{text}```",
        inline=False,
    )

    await ctx.respond(embed=embed)

    example_embed = Greet.message(ctx.author, text)
    return await ctx.send(embed=example_embed, content=ctx.author.mention)
