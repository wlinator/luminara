from discord.ext import commands
from lib.const import CONST
from ui.embeds import builder
from discord import app_commands
import discord
from wrappers.xkcd import Client, HttpError
from typing import Optional

_xkcd = Client()


async def print_comic(
    interaction: discord.Interaction,
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

        await interaction.response.send_message(
            embed=builder.create_embed(
                theme="info",
                author_text=CONST.STRINGS["xkcd_title"].format(comic.id, comic.title),
                description=CONST.STRINGS["xkcd_description"].format(
                    comic.explanation_url,
                    comic.comic_url,
                ),
                footer_text=CONST.STRINGS["xkcd_footer"],
                image_url=comic.image_url,
            ),
        )

    except HttpError:
        await interaction.response.send_message(
            embed=builder.create_embed(
                theme="error",
                author_text=CONST.STRINGS["xkcd_not_found_author"],
                description=CONST.STRINGS["xkcd_not_found"],
                footer_text=CONST.STRINGS["xkcd_footer"],
            ),
        )


class Xkcd(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    xkcd = app_commands.Group(name="xkcd", description="Get the latest xkcd comic")

    @xkcd.command(name="latest", description="Get the latest xkcd comic")
    async def xkcd_latest(self, interaction: discord.Interaction) -> None:
        await print_comic(interaction, latest=True)

    @xkcd.command(name="random", description="Get a random xkcd comic")
    async def xkcd_random(self, interaction: discord.Interaction) -> None:
        await print_comic(interaction)

    @xkcd.command(name="search", description="Search for an xkcd comic")
    async def xkcd_search(self, interaction: discord.Interaction, id: int) -> None:
        await print_comic(interaction, number=id)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Xkcd(bot))
