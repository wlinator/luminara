from datetime import datetime, timedelta

import lib.time
from lib.embed_builder import EmbedBuilder
from services.currency_service import Currency
from services.daily_service import Dailies
from lib.constants import CONST


async def cmd(ctx) -> None:
    ctx_daily = Dailies(ctx.author.id)

    if not ctx_daily.can_be_claimed():
        wait_time = datetime.now() + timedelta(seconds=lib.time.seconds_until(7, 0))
        unix_time = int(round(wait_time.timestamp()))
        error_embed = EmbedBuilder.create_error_embed(
            ctx,
            author_text=CONST.STRINGS["daily_already_claimed_author"],
            description=CONST.STRINGS["daily_already_claimed_description"].format(
                unix_time,
            ),
            footer_text=CONST.STRINGS["daily_already_claimed_footer"],
        )
        await ctx.respond(embed=error_embed)
        return
    ctx_daily.streak = ctx_daily.streak + 1 if ctx_daily.streak_check() else 1
    ctx_daily.claimed_at = datetime.now(tz=ctx_daily.tz)
    ctx_daily.amount = 100 * 12 * (ctx_daily.streak - 1)

    ctx_daily.refresh()

    embed = EmbedBuilder.create_success_embed(
        ctx,
        author_text=CONST.STRINGS["daily_success_claim_author"],
        description=CONST.STRINGS["daily_success_claim_description"].format(
            Currency.format(ctx_daily.amount),
        ),
        footer_text=CONST.STRINGS["daily_streak_footer"].format(ctx_daily.streak)
        if ctx_daily.streak > 1
        else None,
    )

    await ctx.respond(embed=embed)
