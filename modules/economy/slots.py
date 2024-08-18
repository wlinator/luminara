import asyncio
import datetime
import random
from collections import Counter

import discord
import pytz
from discord.ext import commands

from lib.constants import CONST
from services.currency_service import Currency
from services.stats_service import SlotsStats

est = pytz.timezone("US/Eastern")


async def cmd(self, ctx, bet):
    # Currency handler
    ctx_currency = Currency(ctx.author.id)

    # check if the user has enough cash
    player_balance = ctx_currency.balance
    if bet > player_balance:
        raise commands.BadArgument("you don't have enough cash.")
    elif bet <= 0:
        raise commands.BadArgument("the bet you entered is invalid.")

    # # check if the bet exceeds the bet limit
    # bet_limit = int(resources["bet_limit"])
    # if abs(bet) > bet_limit:
    #     message = strings["bet_limit"].format(ctx.author.name, Currency.format_human(bet_limit))
    #     return await ctx.respond(content=message)

    # calculate the results before the command is shown
    results = [random.randint(0, 6) for _ in range(3)]
    calculated_results = calculate_slots_results(bet, results)

    (result_type, payout, multiplier) = calculated_results
    is_won = result_type != "lost"
    # only get the emojis once
    emojis = get_emotes(self.client)

    # start with default "spinning" embed
    await ctx.respond(
        embed=slots_spinning(ctx, 3, Currency.format_human(bet), results, emojis),
    )
    await asyncio.sleep(1)

    for i in range(2, 0, -1):
        await ctx.edit(
            embed=slots_spinning(ctx, i, Currency.format_human(bet), results, emojis),
        )
        await asyncio.sleep(1)

    # output final result
    finished_output = slots_finished(
        ctx,
        result_type,
        Currency.format_human(bet),
        Currency.format_human(payout),
        results,
        emojis,
    )

    await ctx.edit(embed=finished_output)

    # user payout
    if payout > 0:
        ctx_currency.add_balance(payout)
    else:
        ctx_currency.take_balance(bet)

    stats = SlotsStats(
        user_id=ctx.author.id,
        is_won=is_won,
        bet=bet,
        payout=payout,
        spin_type=result_type,
        icons=results,
    )

    ctx_currency.push()
    stats.push()


def get_emotes(client):
    decoration = CONST.SLOTS["emotes"]
    return {name: client.get_emoji(emoji_id) for name, emoji_id in decoration.items()}


def calculate_slots_results(bet, results):
    result_type = None
    multiplier = None
    rewards = CONST.SLOTS["reward_multipliers"]

    # count occurrences of each item in the list
    counts = Counter(results)

    # no icons match
    if len(counts) == 3:
        result_type = "lost"
        multiplier = 0

    elif len(counts) == 2:
        result_type = "pair"
        multiplier = rewards[result_type]

    elif len(counts) == 1:
        if results[0] == 5:
            result_type = "three_diamonds"
        elif results[0] == 6:
            result_type = "jackpot"
        else:
            result_type = "three_of_a_kind"
        multiplier = rewards[result_type]

    payout = bet * multiplier
    return result_type, int(payout), multiplier


def slots_spinning(ctx, spinning_icons_amount, bet, results, emojis):
    first_slots_emote = emojis.get(f"slots_{results[0]}_id")
    second_slots_emote = emojis.get(f"slots_{results[1]}_id")
    slots_animated_emote = emojis.get("slots_animated_id")

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

    description = (
        f"🎰{emojis['S_Wide']}{emojis['L_Wide']}{emojis['O_Wide']}{emojis['T_Wide']}{emojis['S_Wide']}🎰\n"
        f"{emojis['CBorderTLeft']}{emojis['HBorderT']}{emojis['HBorderT']}{emojis['HBorderT']}"
        f"{emojis['HBorderT']}{emojis['HBorderT']}{emojis['CBorderTRight']}\n"
        f"{emojis['VBorder']}{one}{emojis['VBorder']}{two}{emojis['VBorder']}"
        f"{three}{emojis['VBorder']}\n"
        f"{emojis['CBorderBLeft']}{emojis['HBorderB']}{emojis['HBorderB']}{emojis['HBorderB']}"
        f"{emojis['HBorderB']}{emojis['HBorderB']}{emojis['CBorderBRight']}\n"
        f"{emojis['Blank']}{emojis['Blank']}❓❓❓{emojis['Blank']}{emojis['Blank']}{emojis['Blank']}"
    )

    embed = discord.Embed(
        description=description,
    )
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.set_footer(
        text=f"Bet ${bet} • jackpot = x15 • {current_time}",
        icon_url="https://i.imgur.com/wFsgSnr.png",
    )

    return embed


def slots_finished(ctx, payout_type, bet, payout, results, emojis):
    first_slots_emote = emojis.get(f"slots_{results[0]}_id")
    second_slots_emote = emojis.get(f"slots_{results[1]}_id")
    third_slots_emote = emojis.get(f"slots_{results[2]}_id")
    current_time = datetime.datetime.now(est).strftime("%I:%M %p")

    field_name = "You lost."
    field_value = f"You lost **${bet}**."
    color = discord.Color.red()
    is_lost = True

    if payout_type == "pair":
        field_name = "Pair"
        field_value = f"You won **${payout}**."
        is_lost = False
        color = discord.Color.dark_green()
    elif payout_type == "three_of_a_kind":
        field_name = "3 of a kind"
        field_value = f"You won **${payout}**."
        is_lost = False
        color = discord.Color.dark_green()
    elif payout_type == "three_diamonds":
        field_name = "Triple Diamonds!"
        field_value = f"You won **${payout}**."
        is_lost = False
        color = discord.Color.green()
    elif payout_type == "jackpot":
        field_name = "JACKPOT!!"
        field_value = f"You won **${payout}**."
        is_lost = False
        color = discord.Color.green()

    description = (
        f"🎰{emojis['S_Wide']}{emojis['L_Wide']}{emojis['O_Wide']}{emojis['T_Wide']}{emojis['S_Wide']}🎰\n"
        f"{emojis['CBorderTLeft']}{emojis['HBorderT']}{emojis['HBorderT']}{emojis['HBorderT']}"
        f"{emojis['HBorderT']}{emojis['HBorderT']}{emojis['CBorderTRight']}\n"
        f"{emojis['VBorder']}{first_slots_emote}{emojis['VBorder']}{second_slots_emote}"
        f"{emojis['VBorder']}{third_slots_emote}{emojis['VBorder']}\n"
        f"{emojis['CBorderBLeft']}{emojis['HBorderB']}{emojis['HBorderB']}{emojis['HBorderB']}"
        f"{emojis['HBorderB']}{emojis['HBorderB']}{emojis['CBorderBRight']}"
    )

    if is_lost:
        description += (
            f"\n{emojis['Blank']}{emojis['LCentered']}{emojis['OCentered']}{emojis['SCentered']}"
            f"{emojis['ECentered']}{emojis['lost']}{emojis['Blank']}"
        )
    else:
        description += f"\n{emojis['Blank']}🎉{emojis['WSmall']}{emojis['ISmall']}{emojis['NSmall']}🎉{emojis['Blank']}"

    embed = discord.Embed(
        color=color,
        description=description,
    )
    embed.add_field(name=field_name, value=field_value, inline=False)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.set_footer(
        text=f"Game finished • {current_time}",
        icon_url="https://i.imgur.com/wFsgSnr.png",
    )

    return embed
