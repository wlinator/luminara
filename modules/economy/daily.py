from datetime import datetime, timedelta

import lib.time
from lib.embeds.error import EconErrors
from lib.embeds.info import EconInfo
from services.Currency import Currency
from services.Dailies import Dailies


async def cmd(ctx):
    ctx_daily = Dailies(ctx.author.id)

    if not ctx_daily.can_be_claimed():
        wait_time = datetime.now() + timedelta(seconds=lib.time.seconds_until(7, 0))
        unix_time = int(round(wait_time.timestamp()))
        embed = EconErrors.daily_already_claimed(ctx, unix_time)
        return await ctx.respond(embed=embed)

    ctx_daily.streak = ctx_daily.streak + 1 if ctx_daily.streak_check() else 1
    ctx_daily.claimed_at = datetime.now(tz=ctx_daily.tz).isoformat()
    ctx_daily.amount = int(100 * (12 * (ctx_daily.streak - 1)))

    ctx_daily.refresh()

    embed = EconInfo.daily_reward_claimed(ctx, Currency.format(ctx_daily.amount), ctx_daily.streak)

    await ctx.respond(embed=embed)
