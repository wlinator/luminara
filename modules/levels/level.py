from discord import Embed
from discord.ext import commands
from lib.constants import CONST
from lib.embed_builder import EmbedBuilder
from services.xp_service import XpService


async def rank(ctx: commands.Context) -> None:
    xp_data: XpService = XpService(ctx.author.id, ctx.guild.id)

    rank: str = str(xp_data.calculate_rank())
    needed_xp_for_next_level: int = XpService.xp_needed_for_next_level(xp_data.level)

    embed: Embed = EmbedBuilder.create_success_embed(
        ctx=ctx,
        title=CONST.STRINGS["xp_level"].format(xp_data.level),
        footer_text=CONST.STRINGS["xp_server_rank"].format(rank or "NaN"),
        show_name=False,
        thumbnail_url=ctx.author.display_avatar.url,
    )
    embed.add_field(
        name=CONST.STRINGS["xp_progress"],
        value=XpService.generate_progress_bar(xp_data.xp, needed_xp_for_next_level),
        inline=False,
    )

    await ctx.respond(embed=embed, content=ctx.author.mention)
