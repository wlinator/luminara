from discord.ext import commands

import lib.format
from lib.client import Luminara
from lib.const import CONST
from services.currency_service import Currency
from ui.embeds import Builder


class Balance(commands.Cog):
    def __init__(self, bot: Luminara) -> None:
        self.bot: Luminara = bot
        self.balance.usage = lib.format.generate_usage(self.balance)

    @commands.hybrid_command(
        name="balance",
        aliases=["bal", "$"],
    )
    @commands.guild_only()
    async def balance(
        self,
        ctx: commands.Context[Luminara],
    ) -> None:
        """
        Check your current balance.

        Parameters
        ----------
        ctx : commands.Context[Luminara]
            The context of the command.
        """

        ctx_currency = Currency(ctx.author.id)
        balance = Currency.format(ctx_currency.balance)

        embed = Builder.create_embed(
            Builder.SUCCESS,
            user_name=ctx.author.name,
            author_text=CONST.STRINGS["balance_author"].format(ctx.author.name),
            author_icon_url=ctx.author.display_avatar.url,
            description=CONST.STRINGS["balance_cash"].format(balance),
            footer_text=CONST.STRINGS["balance_footer"],
            hide_name_in_description=True,
            hide_time=True,
        )

        await ctx.send(embed=embed)


async def setup(bot: Luminara) -> None:
    await bot.add_cog(Balance(bot))
