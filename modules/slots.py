import asyncio
import datetime
import random
from collections import Counter

import discord
import pytz
from discord.ext import commands

from data.Currency import Currency
from data.SlotsStats import SlotsStats
from handlers.ItemHandler import ItemHandler
from main import economy_config
from sb_tools import economy_embeds, universal

est = pytz.timezone('US/Eastern')


def calculate_slots_results(bet, results):
    type = None
    multiplier = None
    rewards = economy_config["slots"]["reward_multipliers"]

    # count occurrences of each item in the list
    counts = Counter(results)

    # no icons match
    if len(counts) == 3:
        type = "lost"
        multiplier = 0

    # pairs
    elif len(counts) == 2:
        type = "pair"
        multiplier = rewards[type]

    # 3 of a kind
    elif len(counts) == 1:

        if results[0] == 5:
            type = "three_diamonds"
            multiplier = rewards[type]

        elif results[0] == 6:
            type = "jackpot"
            multiplier = rewards[type]

        else:
            type = "three_of_a_kind"
            multiplier = rewards[type]

    payout = bet * multiplier
    return type, int(payout), multiplier


def slots_spinning(ctx, spinning_icons_amount, bet, results, sbbot):
    first_slots_emote = sbbot.get_emoji(economy_config["slots"]["emotes"][f"slots_{results[0]}_id"])
    second_slots_emote = sbbot.get_emoji(economy_config["slots"]["emotes"][f"slots_{results[1]}_id"])
    slots_animated_emote = sbbot.get_emoji(economy_config["slots"]["emotes"][f"slots_animated_id"])

    decoration = economy_config["slots"]["emotes"]
    S_Wide = sbbot.get_emoji(decoration["S_Wide"])
    L_Wide = sbbot.get_emoji(decoration["L_Wide"])
    O_Wide = sbbot.get_emoji(decoration["O_Wide"])
    T_Wide = sbbot.get_emoji(decoration["T_Wide"])

    CBorderBLeft = sbbot.get_emoji(decoration["CBorderBLeft"])
    CBorderBRight = sbbot.get_emoji(decoration["CBorderBRight"])
    CBorderTLeft = sbbot.get_emoji(decoration["CBorderTLeft"])
    CBorderTRight = sbbot.get_emoji(decoration["CBorderTRight"])
    HBorderB = sbbot.get_emoji(decoration["HBorderB"])
    HBorderT = sbbot.get_emoji(decoration["HBorderT"])
    VBorder = sbbot.get_emoji(decoration["VBorder"])

    Blank = sbbot.get_emoji(decoration["Blank"])

    current_time = datetime.datetime.now(est).strftime("%I:%M %p")
    one = slots_animated_emote
    two = slots_animated_emote
    three = slots_animated_emote

    if spinning_icons_amount == 3:
        pass
    elif spinning_icons_amount == 2:
        one = first_slots_emote
    elif spinning_icons_amount == 1:
        one = first_slots_emote
        two = second_slots_emote

    description = f"🎰{S_Wide}{L_Wide}{O_Wide}{T_Wide}{S_Wide}🎰\n" \
                  f"{CBorderTLeft}{HBorderT}{HBorderT}{HBorderT}{HBorderT}{HBorderT}{CBorderTRight}\n" \
                  f"{VBorder}{one}{VBorder}{two}{VBorder}{three}{VBorder}\n" \
                  f"{CBorderBLeft}{HBorderB}{HBorderB}{HBorderB}{HBorderB}{HBorderB}{CBorderBRight}\n" \
                  f"{Blank}{Blank}❓❓❓{Blank}{Blank}{Blank}"

    embed = discord.Embed(
        description=description
    )
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.set_footer(text=f"Bet ${bet} • jackpot = x15 • {current_time}",
                     icon_url="https://i.imgur.com/wFsgSnr.png")

    return embed


def slots_finished(ctx, payout_type, multiplier, bet, payout, results, sbbot):
    first_slots_emote = sbbot.get_emoji(economy_config["slots"]["emotes"][f"slots_{results[0]}_id"])
    second_slots_emote = sbbot.get_emoji(economy_config["slots"]["emotes"][f"slots_{results[1]}_id"])
    third_slots_emote = sbbot.get_emoji(economy_config["slots"]["emotes"][f"slots_{results[2]}_id"])
    current_time = datetime.datetime.now(est).strftime("%I:%M %p")

    decoration = economy_config["slots"]["emotes"]
    S_Wide = sbbot.get_emoji(decoration["S_Wide"])
    L_Wide = sbbot.get_emoji(decoration["L_Wide"])
    O_Wide = sbbot.get_emoji(decoration["O_Wide"])
    T_Wide = sbbot.get_emoji(decoration["T_Wide"])

    CBorderBLeft = sbbot.get_emoji(decoration["CBorderBLeft"])
    CBorderBRight = sbbot.get_emoji(decoration["CBorderBRight"])
    CBorderTLeft = sbbot.get_emoji(decoration["CBorderTLeft"])
    CBorderTRight = sbbot.get_emoji(decoration["CBorderTRight"])
    HBorderB = sbbot.get_emoji(decoration["HBorderB"])
    HBorderT = sbbot.get_emoji(decoration["HBorderT"])
    VBorder = sbbot.get_emoji(decoration["VBorder"])

    WSmall = sbbot.get_emoji(decoration["WSmall"])
    ISmall = sbbot.get_emoji(decoration["ISmall"])
    NSmall = sbbot.get_emoji(decoration["NSmall"])

    LCentered = sbbot.get_emoji(decoration["LCentered"])
    OCentered = sbbot.get_emoji(decoration["OCentered"])
    SCentered = sbbot.get_emoji(decoration["SCentered"])
    ECentered = sbbot.get_emoji(decoration["ECentered"])

    Blank = sbbot.get_emoji(decoration["Blank"])
    lost_emoji = sbbot.get_emoji(decoration["lost"])

    field_name = "You lost."
    field_value = f"You lost **${bet}**."
    color = discord.Color.red()
    is_lost = True

    if payout_type == "pair":
        field_name = "Pair"
        field_value = f"You won **${payout}**."
        is_lost = False
        discord.Color.dark_green()
    elif payout_type == "three_of_a_kind":
        field_name = "3 of a kind"
        field_value = f"You won **${payout}**."
        is_lost = False
        discord.Color.dark_green()
    elif payout_type == "three_diamonds":
        field_name = "Triple Diamonds!"
        field_value = f"You won **${payout}**."
        is_lost = False
        discord.Color.green()
    elif payout_type == "jackpot":
        field_name = "JACKPOT!!"
        field_value = f"You won **${payout}**."
        is_lost = False
        discord.Color.green()

    description = f"🎰{S_Wide}{L_Wide}{O_Wide}{T_Wide}{S_Wide}🎰\n" \
                  f"{CBorderTLeft}{HBorderT}{HBorderT}{HBorderT}{HBorderT}{HBorderT}{CBorderTRight}\n" \
                  f"{VBorder}{first_slots_emote}{VBorder}{second_slots_emote}{VBorder}{third_slots_emote}{VBorder}\n" \
                  f"{CBorderBLeft}{HBorderB}{HBorderB}{HBorderB}{HBorderB}{HBorderB}{CBorderBRight}"

    if is_lost:
        description += f"\n{Blank}{LCentered}{OCentered}{SCentered}{ECentered}{lost_emoji}{Blank}"
    else:
        description += f"\n{Blank}🎉{WSmall}{ISmall}{NSmall}🎉{Blank}"

    embed = discord.Embed(
        color=color,
        description=description
    )
    embed.add_field(name=field_name, value=field_value)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.set_footer(text=f"Bet ${bet} • jackpot = x15 • {current_time}",
                     icon_url="https://i.imgur.com/wFsgSnr.png")

    return embed


class SlotsCog(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot

    @commands.slash_command(
        name="slots",
        descriptions="Spin the slots for a chance to win the jackpot!",
        guild_only=True
    )
    @commands.check(universal.channel_check)
    async def slots(self, ctx, *, bet: discord.Option(int)):

        # Currency handler
        ctx_currency = Currency(ctx.author.id)

        # check if the user has enough cash
        player_cash_balance = ctx_currency.cash
        if bet > player_cash_balance or bet <= 0:
            await ctx.respond(embed=economy_embeds.not_enough_cash())
            return

        # calculate the results before the command is shown
        results = [random.randint(0, 6) for _ in range(3)]
        calculated_results = calculate_slots_results(bet, results)

        (type, payout, multiplier) = calculated_results
        is_won = True

        if type == "lost":
            is_won = False

        # start with default "spinning" embed
        await ctx.respond(embed=slots_spinning(ctx, 3, Currency.format_human(bet), results, self.bot))
        await asyncio.sleep(1)

        for i in range(2, 0, -1):
            await ctx.edit(embed=slots_spinning(ctx, i, Currency.format_human(bet), results, self.bot))
            await asyncio.sleep(1)

        # output final result
        await ctx.edit(embed=slots_finished(ctx, type, multiplier, Currency.format_human(bet),
                                            Currency.format_human(payout), results, self.bot))

        # user payout
        if payout > 0:
            ctx_currency.add_cash(payout)
        else:
            ctx_currency.take_cash(bet)

        item_reward = ItemHandler(ctx)
        await item_reward.rave_coin(is_won=is_won, bet=bet)

        stats = SlotsStats(
            user_id=ctx.author.id,
            is_won=is_won,
            bet=bet,
            payout=payout,
            spin_type=type,
            icons=results
        )

        ctx_currency.push()
        stats.push()


def setup(sbbot):
    sbbot.add_cog(SlotsCog(sbbot))
