from lib.embeds.error import MiscErrors
from lib.embeds.info import MiscInfo
from database.controllers.guild_config import GuildConfigController


async def set_cmd(ctx, prefix):
    if len(prefix) > 25:
        return await ctx.respond(embed=MiscErrors.prefix_too_long(ctx))

    guild_config = GuildConfigController(ctx.guild.id)
    await guild_config.set_prefix(prefix)

    await ctx.respond(embed=MiscInfo.set_prefix(ctx, prefix))


async def get_cmd(ctx):
    guild_config = GuildConfigController(ctx.guild.id)
    prefix = await guild_config.get_prefix()
    await ctx.respond(embed=await MiscInfo.get_prefix(ctx, prefix))
