import logging
from datetime import datetime

import discord
import pytz
from dotenv import load_dotenv

logs = logging.getLogger('Racu.Core')
load_dotenv('.env')
est = pytz.timezone('US/Eastern')


def blackjack_show(ctx, bet, player_hand, dealer_hand, player_hand_value, dealer_hand_value):
    current_time = datetime.now(est).strftime("%I:%M %p")
    thumbnail_url = None

    embed = discord.Embed(
        title="BlackJack",
        color=discord.Color.dark_orange()
    )

    embed.description = f"**You**\n" \
                        f"Score: {player_hand_value}\n" \
                        f"*Hand: {' + '.join(player_hand)}*\n\n"

    if len(dealer_hand) < 2:
        embed.description += f"**Dealer**\n" \
                             f"Score: {dealer_hand_value}\n" \
                             f"*Hand: {dealer_hand[0]} + ??*"
    else:
        embed.description += f"**Dealer | Score: {dealer_hand_value}**\n" \
                             f"*Hand: {' + '.join(dealer_hand)}*"

    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.set_footer(text=f"Bet ${bet} • deck shuffled • Today at {current_time}",
                     icon_url="https://i.imgur.com/96jPPXO.png")

    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)

    return embed


def blackjack_finished(ctx, bet, player_hand_value, dealer_hand_value, payout, status):
    current_time = datetime.now(est).strftime("%I:%M %p")
    thumbnail_url = None

    embed = discord.Embed(
        title="BlackJack"
    )
    embed.description = f"You | Score: {player_hand_value}\n" \
                        f"Dealer | Score: {dealer_hand_value}"
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.set_footer(text=f"Game finished • Today at {current_time}",
                     icon_url="https://i.imgur.com/96jPPXO.png")

    if status == 1:
        name = "Busted.."
        value = f"You lost **${bet}**."
        thumbnail_url = "https://i.imgur.com/rc68c43.png"
        color = discord.Color.red()
    
    elif status == 2:
        name = "You won with a score of 21!"
        value = f"You won **${payout}**."
        thumbnail_url = "https://i.imgur.com/dvIIr2G.png"
        color = discord.Color.green()

    elif status == 3:
        name = "The dealer busted. You won!"
        value = f"You won **${payout}**."
        thumbnail_url = "https://i.imgur.com/dvIIr2G.png"
        color = discord.Color.green()

    elif status == 4:
        name = "You lost.."
        value = f"You lost **${bet}**."
        thumbnail_url = "https://i.imgur.com/rc68c43.png"
        color = discord.Color.red()

    elif status == 5:
        name = "You won with a natural hand!"
        value = f"You won **${payout}**."
        thumbnail_url = "https://i.imgur.com/dvIIr2G.png"
        color = discord.Color.green()

    else:
        name = "I.. don't know if you won?"
        value = "This is an error, please report it."
        color = discord.Color.red()

    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)

    embed.add_field(name=name,
                    value=value,
                    inline=False)
    embed.colour = color

    return embed
