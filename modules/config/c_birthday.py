import discord

from lib.constants import CONST
from lib.embed_builder import EmbedBuilder
from services.config_service import GuildConfig


async def set_birthday_channel(ctx, channel: discord.TextChannel):
    guild_config = GuildConfig(ctx.guild.id)
    guild_config.birthday_channel_id = channel.id
    guild_config.push()

    embed = EmbedBuilder().create_success_embed(
        ctx=ctx,
        author_text=CONST.STRINGS["config_author"],
        description=CONST.STRINGS["config_birthday_channel_set"].format(
            channel.mention,
        ),
    )

    return await ctx.respond(embed=embed)


async def disable_birthday_module(ctx):
    guild_config = GuildConfig(ctx.guild.id)

    if not guild_config.birthday_channel_id:
        embed = EmbedBuilder().create_warning_embed(
            ctx=ctx,
            author_text=CONST.STRINGS["config_author"],
            description=CONST.STRINGS["config_birthday_module_already_disabled"],
        )

    else:
        embed = EmbedBuilder().create_success_embed(
            ctx=ctx,
            author_text=CONST.STRINGS["config_author"],
            description=CONST.STRINGS["config_birthday_module_disabled"],
        )
        guild_config.birthday_channel_id = None
        guild_config.push()

    return await ctx.respond(embed=embed)
