from discord.ext import commands

import lib.format
from lib.client import Luminara
from lib.const import CONST
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
    @commands.is_nsfw()
    async def inspirobot(self, ctx: commands.Context[Luminara]) -> None:
        """
        Get a random AI-generated motivational image from Inspirobot.

        Parameters
        ----------
        ctx : commands.Context[Luminara]
            The context of the command.
        """
        async with ctx.typing():
            try:
                image_url = await InspiroBot().get_image()
            except Exception as e:
                msg = CONST.STRINGS["inspirobot_failed_to_get_image"].format(e)
                raise LumiException(msg) from e

        embed = Builder.create_embed(
            Builder.SUCCESS,
            author_text=CONST.STRINGS["inspirobot_author"],
            image_url=image_url,
        )
        await ctx.send(embed=embed)


async def setup(bot: Luminara) -> None:
    await bot.add_cog(Inspirobot(bot))
