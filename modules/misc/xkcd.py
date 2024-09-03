import discord
from discord import app_commands
from discord.ext import commands

from lib.client import Luminara
from lib.const import CONST
from ui.embeds import Builder
from wrappers.xkcd import Client, HttpError

_xkcd = Client()


async def print_comic(
    interaction: discord.Interaction,
    latest: bool = False,
    number: int | None = None,
) -> None:
    try:
        if latest:
            comic = _xkcd.get_latest_comic(raw_comic_image=True)
        elif number is not None:
            comic = _xkcd.get_comic(number, raw_comic_image=True)
        else:
            comic = _xkcd.get_random_comic(raw_comic_image=True)

        await interaction.response.send_message(
            embed=Builder.create_embed(
                Builder.INFO,
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
            embed=Builder.create_embed(
                Builder.ERROR,
                author_text=CONST.STRINGS["xkcd_not_found_author"],
                description=CONST.STRINGS["xkcd_not_found"],
                footer_text=CONST.STRINGS["xkcd_footer"],
            ),
        )


class Xkcd(commands.Cog):
    def __init__(self, bot: Luminara):
        self.bot = bot

    xkcd = app_commands.Group(name="xkcd", description="Get the latest xkcd comic")

    @xkcd.command(name="latest")
    async def xkcd_latest(self, interaction: discord.Interaction) -> None:
        """
        Get the latest xkcd comic.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction to get the latest comic for.
        """
        await print_comic(interaction, latest=True)

    @xkcd.command(name="random")
    async def xkcd_random(self, interaction: discord.Interaction) -> None:
        """
        Get a random xkcd comic.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction to get the random comic for.
        """
        await print_comic(interaction)

    @xkcd.command(name="search")
    async def xkcd_search(self, interaction: discord.Interaction, comic_id: int) -> None:
        """
        Get a specific xkcd comic.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction to get the comic for.
        comic_id : int
            The ID of the comic to get.
        """
        await print_comic(interaction, number=comic_id)


async def setup(bot: Luminara) -> None:
    await bot.add_cog(Xkcd(bot))
