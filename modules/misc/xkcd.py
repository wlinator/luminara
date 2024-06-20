from discord.ext import commands

from lib.embeds.info import MiscInfo
from services import xkcd_service

_xkcd = xkcd_service.Client()


async def print_comic(ctx, latest=False, number: int = None):
    try:
        if latest:
            comic = _xkcd.get_latest_comic(raw_comic_image=True)
        elif number is not None:
            comic = _xkcd.get_comic(number, raw_comic_image=True)
        else:
            comic = _xkcd.get_random_comic(raw_comic_image=True)

        description = f"[Explainxkcd]({comic.explanation_url}) | [Webpage]({comic.comic_url})"
        embed = MiscInfo.xkcd(comic.id, comic.title, description, comic.image_url)
        return await ctx.respond(embed=embed)

    except xkcd_service.HttpError:
        raise commands.BadArgument("Failed to fetch this comic.")
