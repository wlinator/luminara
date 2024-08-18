from typing import Optional

from discord.ext import bridge

from lib.constants import CONST
from lib.embed_builder import EmbedBuilder
from services.xkcd_service import Client, HttpError

_xkcd = Client()


async def print_comic(
        ctx: bridge.Context,
        latest: bool = False,
        number: Optional[int] = None,
) -> None:
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
                description=CONST.STRINGS["xkcd_description"].format(
                    comic.explanation_url,
                    comic.comic_url,
                ),
                footer_text=CONST.STRINGS["xkcd_footer"],
                image_url=comic.image_url,
                show_name=False,
            ),
        )

    except HttpError:
        await ctx.respond(
            embed=EmbedBuilder.create_error_embed(
                ctx,
                author_text=CONST.STRINGS["xkcd_not_found_author"],
                description=CONST.STRINGS["xkcd_not_found"],
                footer_text=CONST.STRINGS["xkcd_footer"],
            ),
        )
