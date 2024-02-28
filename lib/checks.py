import asyncio
import os

import discord
from dotenv import load_dotenv

load_dotenv('.env')


async def channel(ctx):
    desired_channel_id = 1118587309365940407  # bot-chat in RCU
    owner_id = os.getenv("OWNER_ID")

    if ctx.channel.id != desired_channel_id and ctx.author.id != int(owner_id):
        channel_mention = f"<#{desired_channel_id}>"
        await ctx.respond(f"You can only do that command in {channel_mention}.", ephemeral=True)
        return False

    return True


async def beta_command(ctx):
    owner_id = os.getenv("OWNER_ID")
    if ctx.author.id != int(owner_id):
        embed = discord.Embed(description=f"You can't use this command just yet! It's currently undergoing testing and "
                                          f"fine-tuning to ensure the best experience for all users. Stay tuned for its"
                                          f" official release.",
                              color=discord.Color.red())
        await ctx.respond(embed=embed, ephemeral=True)
        return False

    return True


async def bot_owner(ctx):
    owner_id = os.getenv("OWNER_ID")
    if ctx.author.id != int(owner_id):
        embed = discord.Embed(description=f"Only Esther can do this command.",
                              color=discord.Color.red())
        await ctx.respond(embed=embed, ephemeral=True)
        return False

    return True


async def eightball(message):
    desired_channel_id = 1118587309365940407

    if message.channel.id != desired_channel_id:
        channel_mention = f"<#{desired_channel_id}>"
        bot_reply = await message.reply(f"You can only ask Racu questions in {channel_mention}.")
        await asyncio.sleep(5)
        await bot_reply.delete()
        return False

    return True
