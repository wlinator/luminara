from discord import app_commands
from discord.ext import commands

import lib.format
from lib.client import Luminara
from lib.exceptions import LumiException
from ui.embeds import Builder
from wrappers.inspirobot import InspiroBot


class Inspirobot(commands.Cog):
    def __init__(self, bot: Luminara) -> None:
        self.bot: Luminara = bot
        self.inspirobot.usage = lib.format.generate_usage(self.inspirobot)

    @commands.hybrid_command(
        name="inspirobot",
        aliases=["inspiro", "ib"],
    )
    @app_commands.describe(ephemeral="Whether to send the image ephemerally.")
    @commands.is_nsfw()
    async def inspirobot(self, ctx: commands.Context[Luminara], *, ephemeral: bool = False) -> None:
        """
        Get a random AI-generated motivational image from Inspirobot.

        Parameters
        ----------
        ctx : commands.Context[Luminara]
            The context of the command.
        ephemeral : bool, optional
            Whether to send the image ephemerally. Defaults to False.
        """
        async with ctx.typing():
            try:
                image_url = await InspiroBot().get_image()
            except Exception as e:
                msg = f"Failed to get image URL from Inspirobot: {e}"
                raise LumiException(msg) from e

        embed = Builder.create_embed(
            Builder.SUCCESS,
            author_text="InspiroBot (AI Generated)",
            image_url=image_url,
        )
        await ctx.send(embed=embed, ephemeral=ephemeral)


async def setup(bot: Luminara) -> None:
    await bot.add_cog(Inspirobot(bot))
