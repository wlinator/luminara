import discord
from lib.embed_builder import EmbedBuilder
from lib.constants import CONST
from services.config_service import GuildConfig
import lib.formatter


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
        footer_text=CONST.STRINGS["config_example_next_footer"],
    )
    embed.add_field(
        name=CONST.STRINGS["config_welcome_template_field"],
        value=f"```{text}```",
        inline=False,
    )

    await ctx.respond(embed=embed)

    example_embed = create_greet_embed(ctx.author, text)
    return await ctx.send(embed=example_embed, content=ctx.author.mention)


async def create_greet_embed(member: discord.Member, template: str | None = None):
    embed = discord.Embed(
        color=discord.Color.embed_background(),
        description=CONST.STRINGS["greet_default_description"].format(
            member.guild.name,
        ),
    )
    if template and embed.description is not None:
        embed.description += CONST.STRINGS["greet_template_description"].format(
            lib.formatter.template(template, member.name),
        )

    embed.set_thumbnail(url=member.display_avatar)

    return embed
