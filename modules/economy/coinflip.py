import asyncio
import random

import discord
from discord import app_commands
from discord.ext import commands

import lib.format
from lib.client import Luminara
from lib.const import CONST
from lib.exceptions import LumiException
from ui.embeds import Builder

ACTIVE_COINFLIPS: dict[int, bool] = {}


class Coinflip(commands.Cog):
    def __init__(self, bot: Luminara) -> None:
        self.bot: Luminara = bot
        self.coinflip.usage = lib.format.generate_usage(self.coinflip)

    @commands.command(
        name="coinflip",
        aliases=["cf"],
    )
    @commands.guild_only()
    async def coinflip(
        self,
        ctx: commands.Context[Luminara],
        *,
        prediction: str | None = None,
    ) -> None:
        """
        Flip a coin. Optionally predict the outcome.

        Parameters
        ----------
        ctx : commands.Context[Luminara]
            The context of the command.
        prediction : str, optional
            The predicted outcome ('heads', 'h', 'tails', or 't').
        """
        if prediction:
            prediction = prediction.lower()
            if prediction in ["h", "head"]:
                prediction = "heads"
            elif prediction in ["t", "tail"]:
                prediction = "tails"

        await self._coinflip(ctx, prediction)

    @app_commands.command(name="coinflip", description="Flip a coin. Optionally predict the outcome.")
    @app_commands.guild_only()
    @app_commands.choices(
        prediction=[
            app_commands.Choice(name="Heads", value="heads"),
            app_commands.Choice(name="Tails", value="tails"),
        ],
    )
    async def coinflip_slash(
        self,
        interaction: discord.Interaction,
        prediction: app_commands.Choice[str] | None = None,
    ) -> None:
        """
        Flip a coin. Optionally predict the outcome.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction of the command.
        prediction : app_commands.Choice[str], optional
            The predicted outcome ('heads' or 'tails').
        """
        await self._coinflip(interaction, prediction.value if prediction else None)

    async def _coinflip(self, ctx: commands.Context[Luminara] | discord.Interaction, prediction: str | None) -> None:
        if isinstance(ctx, commands.Context):
            author = ctx.author
            reply = ctx.reply
        else:
            author = ctx.user
            reply = ctx.followup.send

        if author.id in ACTIVE_COINFLIPS:
            raise LumiException(CONST.STRINGS["error_already_flipping_coin_description"])

        ACTIVE_COINFLIPS[author.id] = True

        try:
            result = random.choice(["heads", "tails"])

            if prediction and prediction not in ["heads", "tails"]:
                raise LumiException(CONST.STRINGS["coinflip_invalid_prediction_description"])

            flip_embed = Builder.create_embed(
                Builder.INFO,
                user_name=author.name,
                author_text=CONST.STRINGS["coinflip_flipping_author"],
                description=CONST.STRINGS["coinflip_flipping_description"],
            )

            if isinstance(ctx, commands.Context):
                flip_message = await reply(embed=flip_embed)
            else:
                await ctx.response.send_message(embed=flip_embed)
                flip_message = await ctx.original_response()

            await asyncio.sleep(1)

            if flip_message is not None:
                flip_embed.description = f"**{author.name}** " + CONST.STRINGS["coinflip_flipping_animation_1"]
                await flip_message.edit(embed=flip_embed)
                await asyncio.sleep(0.5)

                flip_embed.description = f"**{author.name}** " + CONST.STRINGS["coinflip_flipping_animation_2"]
                await flip_message.edit(embed=flip_embed)
                await asyncio.sleep(0.5)

                flip_embed.description = f"**{author.name}** " + CONST.STRINGS["coinflip_flipping_animation_3"]
                await flip_message.edit(embed=flip_embed)
                await asyncio.sleep(0.5)

            if prediction:
                predicted_correctly = prediction == result

                embed_type = Builder.SUCCESS if predicted_correctly else Builder.ERROR
                author_text = CONST.STRINGS[
                    "coinflip_correct_prediction_author" if predicted_correctly else "coinflip_wrong_prediction_author"
                ]
                description = CONST.STRINGS[
                    "coinflip_correct_prediction_description"
                    if predicted_correctly
                    else "coinflip_wrong_prediction_description"
                ].format(result)

                embed = Builder.create_embed(
                    embed_type,
                    user_name=author.name,
                    author_text=author_text,
                    description=description,
                )
            else:
                embed = Builder.create_embed(
                    Builder.INFO,
                    user_name=author.name,
                    author_text=CONST.STRINGS["coinflip_result_author"],
                    description=CONST.STRINGS["coinflip_result_description"].format(result),
                )

            if flip_message is not None:
                await flip_message.edit(embed=embed)
        finally:
            del ACTIVE_COINFLIPS[author.id]


async def setup(bot: Luminara) -> None:
    await bot.add_cog(Coinflip(bot))
