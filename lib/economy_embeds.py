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
