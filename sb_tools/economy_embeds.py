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

    elif status == "player_won_21":
        title_text = "YOU WON!"
        thumbnail_url = "https://i.imgur.com/dvIIr2G.png"
        color = discord.Color.green()

    elif status == "player_blackjack":
        you_text = "You | BlackJack"
        title_text = "YOU WON!"
        thumbnail_url = "https://i.imgur.com/dvIIr2G.png"
        color = discord.Color.green()

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
