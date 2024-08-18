import discord

from lib.constants import CONST
from lib.embed_builder import EmbedBuilder
from lib.exceptions.LumiExceptions import LumiException
from services.moderation.modlog_service import ModLogService


async def set_mod_log_channel(ctx, channel: discord.TextChannel):
    mod_log = ModLogService()

    info_embed = EmbedBuilder().create_success_embed(
        ctx=ctx,
        author_text=CONST.STRINGS["config_modlog_info_author"],
        description=CONST.STRINGS["config_modlog_info_description"].format(
            ctx.guild.name,
        ),
        show_name=False,
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

    mod_log.set_modlog_channel(ctx.guild.id, channel.id)

    success_embed = EmbedBuilder().create_success_embed(
        ctx=ctx,
        author_text=CONST.STRINGS["config_author"],
        description=CONST.STRINGS["config_modlog_channel_set"].format(channel.mention),
    )

    return await ctx.respond(embed=success_embed)
