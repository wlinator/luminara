from lib.embed_builder import EmbedBuilder
from lib.constants import CONST
from services.config_service import GuildConfig


async def set_prefix(ctx, prefix):
    if len(prefix) > 25:
        embed = EmbedBuilder().create_error_embed(
            ctx=ctx,
            author_text=CONST.STRINGS["config_author"],
            description=CONST.STRINGS["config_prefix_too_long"],
        )
        return await ctx.respond(embed=embed)

    guild_config = GuildConfig(
        ctx.guild.id,
    )  # generate a guild_config for if it didn't already exist
    GuildConfig.set_prefix(guild_config.guild_id, prefix)

    embed = EmbedBuilder().create_success_embed(
        ctx=ctx,
        author_text=CONST.STRINGS["config_author"],
        description=CONST.STRINGS["config_prefix_set"].format(prefix),
    )
    await ctx.respond(embed=embed)


async def get_prefix(ctx):
    prefix = GuildConfig.get_prefix_from_guild_id(ctx.guild.id) if ctx.guild else "."
    embed = EmbedBuilder().create_info_embed(
        ctx=ctx,
        author_text=CONST.STRINGS["config_author"],
        description=CONST.STRINGS["config_prefix_get"].format(prefix),
    )
    await ctx.respond(embed=embed)
