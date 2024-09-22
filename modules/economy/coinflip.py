import asyncio
import random

from discord.ext import commands

import lib.format
from lib.client import Luminara
from lib.const import CONST
from ui.embeds import Builder


class Coinflip(commands.Cog):
    def __init__(self, bot: Luminara) -> None:
        self.bot: Luminara = bot
        self.coinflip.usage = lib.format.generate_usage(self.coinflip)

    @commands.hybrid_command(
        name="coinflip",
        aliases=["cf"],
    )
    @commands.guild_only()
    async def coinflip(
        self,
        ctx: commands.Context[Luminara],
        prediction: str | None = None,
    ) -> None:
        """
        Flip a coin. Optionally predict the outcome.

        Parameters
        ----------
        ctx : commands.Context[Luminara]
            The context of the command.
        prediction : str, optional
            The predicted outcome ('heads'/'h' or 'tails'/'t').
        """
        result = random.choice(["heads", "tails"])

        if prediction:
            prediction = prediction.lower()
            if prediction not in ["heads", "h", "tails", "t"]:
                embed = Builder.create_embed(
                    Builder.ERROR,
                    user_name=ctx.author.name,
                    author_text=CONST.STRINGS["coinflip_invalid_prediction_author"],
                    description=CONST.STRINGS["coinflip_invalid_prediction_description"],
                )
                await ctx.send(embed=embed)
                return

        flip_embed = Builder.create_embed(
            Builder.INFO,
            user_name=ctx.author.name,
            author_text=CONST.STRINGS["coinflip_flipping_author"],
            description=CONST.STRINGS["coinflip_flipping_description"],
        )
        flip_message = await ctx.send(embed=flip_embed)

        await asyncio.sleep(1)

        for animation in (
            CONST.STRINGS["coinflip_flipping_animation_1"],
            CONST.STRINGS["coinflip_flipping_animation_2"],
            CONST.STRINGS["coinflip_flipping_animation_3"],
        ):
            flip_embed = Builder.create_embed(
                Builder.INFO,
                user_name=ctx.author.name,
                author_text=CONST.STRINGS["coinflip_flipping_author"],
                description=animation,
            )
            await flip_message.edit(embed=flip_embed)
            await asyncio.sleep(0.5)

        if prediction:
            predicted_correctly = (prediction.startswith("h") and result == "heads") or (
                prediction.startswith("t") and result == "tails"
            )
            if predicted_correctly:
                embed = Builder.create_embed(
                    Builder.SUCCESS,
                    user_name=ctx.author.name,
                    author_text=CONST.STRINGS["coinflip_correct_prediction_author"],
                    description=CONST.STRINGS["coinflip_correct_prediction_description"].format(result),
                )
            else:
                embed = Builder.create_embed(
                    Builder.ERROR,
                    user_name=ctx.author.name,
                    author_text=CONST.STRINGS["coinflip_wrong_prediction_author"],
                    description=CONST.STRINGS["coinflip_wrong_prediction_description"].format(result),
                )
        else:
            embed = Builder.create_embed(
                Builder.INFO,
                user_name=ctx.author.name,
                author_text=CONST.STRINGS["coinflip_result_author"],
                description=CONST.STRINGS["coinflip_result_description"].format(result),
            )

        await flip_message.edit(embed=embed)


async def setup(bot: Luminara) -> None:
    await bot.add_cog(Coinflip(bot))
