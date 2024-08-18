from typing import Optional

import discord
from discord.ext.commands import MemberConverter

from lib import formatter
from lib.constants import CONST
from lib.embed_builder import EmbedBuilder
from lib.exceptions.LumiExceptions import LumiException
from services.config_service import GuildConfig


async def set_welcome_channel(ctx, channel: discord.TextChannel) -> None:
    if not ctx.guild:
        raise LumiException()

    guild_config: GuildConfig = GuildConfig(ctx.guild.id)
    guild_config.welcome_channel_id = channel.id
    guild_config.push()

    embed: discord.Embed = EmbedBuilder().create_success_embed(
        ctx=ctx,
        author_text=CONST.STRINGS["config_author"],
        description=CONST.STRINGS["config_welcome_channel_set"].format(channel.mention),
    )

    await ctx.respond(embed=embed)


async def disable_welcome_module(ctx) -> None:
    guild_config: GuildConfig = GuildConfig(ctx.guild.id)

    if not guild_config.welcome_channel_id:
        embed: discord.Embed = EmbedBuilder().create_warning_embed(
            ctx=ctx,
            author_text=CONST.STRINGS["config_author"],
            description=CONST.STRINGS["config_welcome_module_already_disabled"],
        )
    else:
        guild_config.welcome_channel_id = None
        guild_config.welcome_message = None
        guild_config.push()
        embed: discord.Embed = EmbedBuilder().create_success_embed(
            ctx=ctx,
            author_text=CONST.STRINGS["config_author"],
            description=CONST.STRINGS["config_welcome_module_disabled"],
        )

    await ctx.respond(embed=embed)


async def set_welcome_template(ctx, text: str) -> None:
    if not ctx.guild:
        raise LumiException()

    guild_config: GuildConfig = GuildConfig(ctx.guild.id)
    guild_config.welcome_message = text
    guild_config.push()

    embed: discord.Embed = EmbedBuilder().create_success_embed(
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

    greet_member: discord.Member = await MemberConverter().convert(ctx, str(ctx.author))
    example_embed: discord.Embed = create_greet_embed(greet_member, text)
    await ctx.send(embed=example_embed, content=ctx.author.mention)


def create_greet_embed(
        member: discord.Member,
        template: Optional[str] = None,
) -> discord.Embed:
    embed: discord.Embed = discord.Embed(
        color=discord.Color.embed_background(),
        description=CONST.STRINGS["greet_default_description"].format(
            member.guild.name,
        ),
    )
    if template and embed.description is not None:
        embed.description += CONST.STRINGS["greet_template_description"].format(
            formatter.template(template, member.name),
        )

    embed.set_thumbnail(url=member.display_avatar.url)

    return embed
