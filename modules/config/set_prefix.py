from lib.embeds.error import MiscErrors
from lib.embeds.info import MiscInfo
from services.GuildConfig import GuildConfig


async def set_cmd(ctx, prefix):
    if len(prefix) > 25:
        return await ctx.respond(embed=MiscErrors.prefix_too_long(ctx))

    guild_config = GuildConfig(ctx.guild.id)  # generate a guild_config for if it didn't already exist
    GuildConfig.set_prefix(guild_config.guild_id, prefix)

    await ctx.respond(embed=MiscInfo.set_prefix(ctx, prefix))


async def get_cmd(ctx):
    prefix = GuildConfig.get_prefix(ctx.guild.id)
    await ctx.respond(embed=MiscInfo.get_prefix(ctx, prefix))
