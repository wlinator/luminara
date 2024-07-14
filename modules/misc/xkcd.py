from services import xkcd_service
from lib.embed_builder import EmbedBuilder
from lib.constants import CONST
from discord.ext import bridge
from typing import Union

_xkcd = xkcd_service.Client()


async def print_comic(ctx: bridge.Context, latest: bool = False, number: Union[int, None] = None) -> None:
    try:
        if latest:
            comic = _xkcd.get_latest_comic(raw_comic_image=True)
        elif number is not None:
            comic = _xkcd.get_comic(number, raw_comic_image=True)
        else:
            comic = _xkcd.get_random_comic(raw_comic_image=True)

        await ctx.respond(
            embed=EmbedBuilder.create_success_embed(
                ctx,
                author_text=CONST.STRINGS["xkcd_title"].format(comic.id, comic.title),
                description=CONST.STRINGS["xkcd_description"].format(comic.explanation_url, comic.comic_url),
                footer_text=CONST.STRINGS["xkcd_footer"],
                image_url=comic.image_url,
                show_name=False,
            )
        )

    except xkcd_service.HttpError:
        await ctx.respond(
            embed=EmbedBuilder.create_error_embed(
                ctx,
                author_text=CONST.STRINGS["xkcd_not_found_author"],
                description=CONST.STRINGS["xkcd_not_found"],
                footer_text=CONST.STRINGS["xkcd_footer"],
            )
        )
