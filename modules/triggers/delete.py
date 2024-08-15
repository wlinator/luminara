from discord.ext import bridge
from services.reactions_service import CustomReactionsService
from lib.embed_builder import EmbedBuilder
from lib.constants import CONST
from lib.exceptions.LumiExceptions import LumiException


async def delete_reaction(ctx: bridge.Context, reaction_id: int) -> None:
    if ctx.guild is None:
        return

    reaction_service = CustomReactionsService()
    guild_id: int = ctx.guild.id
    reaction = await reaction_service.find_id(reaction_id)

    if reaction is None or reaction["guild_id"] != guild_id or reaction["is_global"]:
        raise LumiException(CONST.STRINGS["triggers_not_found"])

    await reaction_service.delete_custom_reaction(reaction_id)

    embed = EmbedBuilder.create_success_embed(
        ctx,
        author_text=CONST.STRINGS["triggers_delete_author"],
        description=CONST.STRINGS["triggers_delete_description"],
        footer_text=CONST.STRINGS["triggers_reaction_service_footer"],
    )

    await ctx.respond(embed=embed)
