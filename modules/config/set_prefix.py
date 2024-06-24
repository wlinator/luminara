from lib.embeds.error import MiscErrors
from lib.embeds.info import MiscInfo
from services.config_service import GuildConfig
from database.controllers.guild_config import GuildConfigController


async def set_cmd(ctx, prefix):
    if len(prefix) > 25:
        return await ctx.respond(embed=MiscErrors.prefix_too_long(ctx))

    guild_config = GuildConfigController()
    await guild_config.set_prefix(ctx.guild.id, prefix)

    await ctx.respond(embed=MiscInfo.set_prefix(ctx, prefix))


async def get_cmd(ctx):
    prefix = GuildConfig.get_prefix(ctx.guild.id)
    await ctx.respond(embed=MiscInfo.get_prefix(ctx, prefix))
