import discord
from lib.constants import CONST
from lib.embed_builder import EmbedBuilder
from services.currency_service import Currency


async def cmd(ctx, user: discord.User, amount: int):
    # Currency handler
    curr = Currency(user.id)
    curr.add_balance(amount)
    curr.push()

    embed = EmbedBuilder.create_success_embed(
        ctx,
        author_text=CONST.STRINGS["admin_award_title"],
        description=CONST.STRINGS["admin_award_description"].format(
            Currency.format(amount),
            user.name,
        ),
    )

    await ctx.respond(embed=embed)
