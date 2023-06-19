import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv('.env')


async def channel_check(ctx):
    desired_channel_id = 1118587309365940407  # bot-chat in RCU
    owner_id = os.getenv("OWNER_ID")

    if ctx.channel.id != desired_channel_id and ctx.author.id != int(owner_id):
        channel_mention = f"<#{desired_channel_id}>"
        await ctx.respond(f"You can only do that command in {channel_mention}.", ephemeral=True)
        return False

    return True


async def beta_check(ctx):
    owner_id = os.getenv("OWNER_ID")
    if ctx.author.id != int(owner_id):
        embed = discord.Embed(description=f"You can't use this command just yet! It's currently undergoing testing and "
                                          f"fine-tuning to ensure the best experience for all users. Stay tuned for its "
                                          f"official release.",
                              color=discord.Color.red())
        await ctx.respond(embed=embed)
        return False

    return True


async def owner_check(ctx):
    owner_id = os.getenv("OWNER_ID")
    if ctx.author.id != int(owner_id):
        embed = discord.Embed(description=f"Only Tess can do this command.",
                              color=discord.Color.red())
        await ctx.respond(embed=embed)
        return False

    return True
