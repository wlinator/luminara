from discord.ext import commands

from services.currency_service import Currency
from lib.constants import CONST
from lib.embed_builder import EmbedBuilder


async def cmd(ctx: commands.Context[commands.Bot]) -> None:
    ctx_currency = Currency(ctx.author.id)
    balance = Currency.format(ctx_currency.balance)

    embed = EmbedBuilder.create_success_embed(
        ctx,
        author_text=CONST.STRINGS["balance_author"].format(ctx.author.name),
        author_icon_url=ctx.author.display_avatar.url,
        description=CONST.STRINGS["balance_cash"].format(balance),
        footer_text=CONST.STRINGS["balance_footer"],
        show_name=False,
        hide_timestamp=True,
    )

    await ctx.respond(embed=embed)
