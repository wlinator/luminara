import json
import os

import discord
import pytz
from dotenv import load_dotenv

load_dotenv('.env')
est = pytz.timezone('US/Eastern')

with open("config/economy.json") as file:
    json_data = json.load(file)


def give_bot_error():
    embed = discord.Embed(
        color=discord.Color.red(),
        description=f"You can't give money to a bot, silly."
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


def out_of_time():
    embed = discord.Embed(
        color=discord.Color.red(),
        description="Uh-oh! Time's up. Your bet is forfeited as the game concludes."
    )
    return embed
