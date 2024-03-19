import os

import discord
from dotenv import load_dotenv
from lib.embeds.error import BdayErrors, GenericErrors
from services.GuildConfig import GuildConfig

load_dotenv('.env')


async def birthday_module(ctx):
    """
        Whether the Birthday module is enabled in a server depends on the field "birthday_channel_id" in racudb.server_config
        NULL or INVALID: disabled
    """
    guild_config = GuildConfig(ctx.guild.id)

    if not guild_config.birthday_channel_id:
        await ctx.respond(embed=BdayErrors.birthdays_disabled(ctx))
        return False
    
    return True


async def channel(ctx):

    if ctx.guild is None:
        return True

    guild_config = GuildConfig(ctx.guild.id)
    command_channel_id = guild_config.command_channel_id

    if command_channel_id:
        if ctx.channel.id != command_channel_id:

            try:
                command_channel = await ctx.guild.fetch_channel(command_channel_id)
                await ctx.respond(embed=GenericErrors.channel_not_allowed(ctx, command_channel),
                                  delete_after=5, ephemeral=True)
                return False

            except (discord.HTTPException, discord.NotFound):
                return True

            except discord.Forbidden:
                return False

    return True


async def bot_owner(ctx):
    owner_id = os.getenv("OWNER_ID")

    if ctx.author.id != int(owner_id):
        await ctx.respond(embed=GenericErrors.owner_only(ctx))
        return False

    return True
