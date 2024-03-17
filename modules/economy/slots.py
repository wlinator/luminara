import datetime
from collections import Counter

import discord
import pytz

from main import economy_config

est = pytz.timezone('US/Eastern')


def get_emotes(client):
    decoration = economy_config["slots"]["emotes"]
    emojis = {name: client.get_emoji(emoji_id) for name, emoji_id in decoration.items()}
    return emojis


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

    description = f"🎰{emojis['S_Wide']}{emojis['L_Wide']}{emojis['O_Wide']}{emojis['T_Wide']}{emojis['S_Wide']}🎰\n" \
                  f"{emojis['CBorderTLeft']}{emojis['HBorderT']}{emojis['HBorderT']}{emojis['HBorderT']}" \
                  f"{emojis['HBorderT']}{emojis['HBorderT']}{emojis['CBorderTRight']}\n" \
                  f"{emojis['VBorder']}{one}{emojis['VBorder']}{two}{emojis['VBorder']}" \
                  f"{three}{emojis['VBorder']}\n" \
                  f"{emojis['CBorderBLeft']}{emojis['HBorderB']}{emojis['HBorderB']}{emojis['HBorderB']}" \
                  f"{emojis['HBorderB']}{emojis['HBorderB']}{emojis['CBorderBRight']}\n" \
                  f"{emojis['Blank']}{emojis['Blank']}❓❓❓{emojis['Blank']}{emojis['Blank']}{emojis['Blank']}"

    embed = discord.Embed(
        description=description
    )
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.set_footer(text=f"Bet ${bet} • jackpot = x15 • {current_time}",
                     icon_url="https://i.imgur.com/wFsgSnr.png")

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

    description = f"🎰{emojis['S_Wide']}{emojis['L_Wide']}{emojis['O_Wide']}{emojis['T_Wide']}{emojis['S_Wide']}🎰\n" \
                  f"{emojis['CBorderTLeft']}{emojis['HBorderT']}{emojis['HBorderT']}{emojis['HBorderT']}" \
                  f"{emojis['HBorderT']}{emojis['HBorderT']}{emojis['CBorderTRight']}\n" \
                  f"{emojis['VBorder']}{first_slots_emote}{emojis['VBorder']}{second_slots_emote}" \
                  f"{emojis['VBorder']}{third_slots_emote}{emojis['VBorder']}\n" \
                  f"{emojis['CBorderBLeft']}{emojis['HBorderB']}{emojis['HBorderB']}{emojis['HBorderB']}" \
                  f"{emojis['HBorderB']}{emojis['HBorderB']}{emojis['CBorderBRight']}"

    if is_lost:
        description += f"\n{emojis['Blank']}{emojis['LCentered']}{emojis['OCentered']}{emojis['SCentered']}" \
                       f"{emojis['ECentered']}{emojis['lost']}{emojis['Blank']}"
    else:
        description += f"\n{emojis['Blank']}🎉{emojis['WSmall']}{emojis['ISmall']}{emojis['NSmall']}🎉{emojis['Blank']}"

    embed = discord.Embed(
        color=color,
        description=description
    )
    embed.add_field(name=field_name, value=field_value, inline=False)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.set_footer(text=f"Game finished • {current_time}",
                     icon_url="https://i.imgur.com/wFsgSnr.png")

    return embed
