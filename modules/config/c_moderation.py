import discord
from lib.embed_builder import EmbedBuilder
from lib.constants import CONST
from services.moderation.modlog_service import ModLogService


async def set_mod_log_channel(ctx, channel: discord.TextChannel):
    mod_log = ModLogService()
    mod_log.set_modlog_channel(ctx.guild.id, channel.id)

    embed = EmbedBuilder().create_success_embed(
        ctx=ctx,
        author_text=CONST.STRINGS["config_author"],
        description=CONST.STRINGS["config_modlog_channel_set"].format(channel.mention),
    )

    return await ctx.respond(embed=embed)
