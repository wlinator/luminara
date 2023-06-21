import datetime
import json
import os

import discord
import pytz
from dotenv import load_dotenv

load_dotenv('.env')

cash_balance_name = os.getenv("CASH_BALANCE_NAME")
special_balance_name = os.getenv("SPECIAL_BALANCE_NAME")
est = pytz.timezone('US/Eastern')

with open("config/economy.json") as file:
    json_data = json.load(file)


def currency_balance(ctx, cash_balance, special_balance):
    embed = discord.Embed(
        description=f"**Cash**: {cash_balance_name}{cash_balance}\n"
                    f"**{special_balance_name.capitalize()}**: {special_balance}"
    )
    embed.set_author(name=f"{ctx.author.name}'s wallet", icon_url=ctx.author.avatar.url)
    embed.set_footer(text=f"Level up to earn {special_balance_name}!")
    return embed


def award(user, currency, amount):
    reward = f"{amount}"
    if currency == "cash_balance":
        reward = cash_balance_name + reward
    else:
        reward = f"{reward} {special_balance_name}"

    embed = discord.Embed(
        color=discord.Color.green(),
        description=f"Awarded **{reward}** to {user.name}."
    )
    return embed


def give(ctx, user, currency, amount):
    reward = f"{amount}"
    if currency == "cash":
        reward = cash_balance_name + reward
    else:
        reward = f"{reward} {special_balance_name}"

    embed = discord.Embed(
        color=discord.Color.green(),
        description=f"**{ctx.author.name}** gave **{reward}** to {user.name}."
    )
    embed.set_footer(text="Say thanks! :)")
    return embed


def give_yourself_error(currency):
    embed = discord.Embed(
        color=discord.Color.red(),
        description=f"You can't give {currency} to yourself, silly."
    )
    return embed


def give_bot_error(currency):
    embed = discord.Embed(
        color=discord.Color.red(),
        description=f"You can't give {currency} to a bot, silly."
    )
    return embed


def already_playing(game):
    embed = discord.Embed(
        color=discord.Color.red(),
        description=f"You're already playing {game}. Please finish this game first."
    )
    return embed


def not_enough_cash():
    embed = discord.Embed(
        color=discord.Color.red(),
        description="Oops! Your current cash balance isn't sufficient to do that."
    )
    return embed


def not_enough_special_balance():
    embed = discord.Embed(
        color=discord.Color.red(),
        description=f"Oops! Your current {special_balance_name} balance isn't sufficient to do that."
    )
    return embed


def out_of_time():
    embed = discord.Embed(
        color=discord.Color.red(),
        description="Uh-oh! Time's up. Your bet is forfeited as the game concludes."
    )
    return embed


def exchange_confirmation(amount):
    embed = discord.Embed(
        description=f"You're about to sell {amount} {special_balance_name} for {cash_balance_name}{amount * 1000}. "
                    f"Are you absolutely sure about this? Keep in mind that repurchasing {special_balance_name} "
                    f"later is considerably more expensive."
    )
    return embed


def exchange_done(amount):
    embed = discord.Embed(
        color=discord.Color.green(),
        description=f"You successfully exchanged **{amount} {special_balance_name}** "
                    f"for **{cash_balance_name}{amount * 1000}**."
    )
    return embed


def exchange_stopped():
    embed = discord.Embed(
        color=discord.Color.red(),
        description="The exchange was canceled because you clicked \"Stop\" or ran out of time."
    )
    return embed


def coinflip(ctx, guess_side, throw_side, bet):
    embed = discord.Embed(
        title=f"You bet {cash_balance_name}{bet} on {guess_side}."
    )
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)

    if throw_side == "heads":
        embed.set_thumbnail(url="https://media.tenor.com/nEu74vu_sT4AAAAC/heads-coinflip.gif")
    else:
        embed.set_thumbnail(url="https://media.tenor.com/kK8D7hQXX5wAAAAC/coins-tails.gif")

    return embed


def coinflip_finished(side, status):
    color = None

    if status == "success":
        color = discord.Color.green()


def blackjack_show(ctx, bet, player_hand, dealer_hand, player_hand_value, dealer_hand_value, status):
    current_time = datetime.datetime.now(est).strftime("%I:%M %p")
    you_text = "You"
    dealer_text = "Dealer"
    title_text = "BlackJack"
    thumbnail_url = None
    color = discord.Color.dark_orange()

    if status == "player_busted":
        you_text = "You | BUSTED"
        title_text = "YOU LOST!"
        thumbnail_url = "https://i.imgur.com/rc68c43.png"
        color = discord.Color.red()

    elif status == "dealer_busted":
        dealer_text = "Dealer | BUSTED"
        title_text = "YOU WON!"
        thumbnail_url = "https://i.imgur.com/dvIIr2G.png"
        color = discord.Color.green()

    elif status == "dealer_won":
        title_text = "YOU LOST!"
        thumbnail_url = "https://i.imgur.com/rc68c43.png"
        color = discord.Color.red()

    embed = discord.Embed(
        title=title_text,
        color=color
    )
    embed.add_field(name=you_text, value=f"**Score: {player_hand_value}**\n"
                                         f"*Hand: {' + '.join(player_hand)}*")

    if len(dealer_hand) < 2:
        embed.add_field(name=dealer_text, value=f"**Score: {dealer_hand_value}**\n"
                                                f"*Hand: {dealer_hand[0]} + ??*", inline=False)
    else:
        embed.add_field(name=dealer_text, value=f"**Score: {dealer_hand_value}**\n"
                                                f"*Hand: {' + '.join(dealer_hand)}*", inline=False)

    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.set_footer(text=f"Bet {cash_balance_name}{bet} • deck shuffled • Today at {current_time}",
                     icon_url="https://i.imgur.com/96jPPXO.png")

    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)

    return embed


def slots_spinning(ctx, spinning_icons_amount, bet, results, sbbot):
    first_slots_emote = sbbot.get_emoji(json_data["slots"]["emotes"][f"slots_{results[0]}_id"])
    second_slots_emote = sbbot.get_emoji(json_data["slots"]["emotes"][f"slots_{results[1]}_id"])
    slots_animated_emote = sbbot.get_emoji(json_data["slots"]["emotes"][f"slots_animated_id"])

    decoration = json_data["slots"]["emotes"]
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
    embed.set_footer(text=f"Bet {cash_balance_name}{bet} • jackpot = x5 • {current_time}",
                     icon_url="https://i.imgur.com/wFsgSnr.png")

    return embed


def slots_finished(ctx, payout_type, multiplier, bet, results, sbbot):
    first_slots_emote = sbbot.get_emoji(json_data["slots"]["emotes"][f"slots_{results[0]}_id"])
    second_slots_emote = sbbot.get_emoji(json_data["slots"]["emotes"][f"slots_{results[1]}_id"])
    third_slots_emote = sbbot.get_emoji(json_data["slots"]["emotes"][f"slots_{results[2]}_id"])
    current_time = datetime.datetime.now(est).strftime("%I:%M %p")

    decoration = json_data["slots"]["emotes"]
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
    field_value = f"You lost **{cash_balance_name}{bet}**."
    color = discord.Color.red()
    is_lost = True

    if payout_type == "pair":
        field_name = "Pair"
        field_value = f"You won **{cash_balance_name}{bet * multiplier}**."
        is_lost = False
        discord.Color.dark_green()
    elif payout_type == "three_of_a_kind":
        field_name = "3 of a kind"
        field_value = f"You won **{cash_balance_name}{bet * multiplier}**."
        is_lost = False
        discord.Color.dark_green()
    elif payout_type == "three_diamonds":
        field_name = "Triple Diamonds!"
        field_value = f"You won **{cash_balance_name}{bet * multiplier}**."
        is_lost = False
        discord.Color.green()
    elif payout_type == "jackpot":
        field_name = "JACKPOT!!"
        field_value = f"You won **{cash_balance_name}{bet * multiplier}**."
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
    embed.set_footer(text=f"Bet {cash_balance_name}{bet} • jackpot = x5 • {current_time}",
                     icon_url="https://i.imgur.com/wFsgSnr.png")

    return embed


def daily_claim(amount, streak):
    embed = discord.Embed(
        color=discord.Color.green(),
        description=f"You claimed your daily reward of **{cash_balance_name}{amount}**."
    )

    if streak > 1:
        embed.set_footer(text=f"You're on a streak of {streak} days!")

    return embed


def daily_wait():
    embed = discord.Embed(
        color=discord.Color.red(),
        description=f"You've already claimed your daily reward."
    )
    embed.set_footer(text="Reset is at 7 AM Eastern!")

    return embed
