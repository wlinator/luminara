import logging

from discord.ext import commands
import discord

from sb_tools import universal
from main import economy_config
import pytz
from datetime import datetime

racu_logs = logging.getLogger('Racu.Core')
est = pytz.timezone('US/Eastern')

logging_channel_id = 1191707328148418611
rc_guild_id = economy_config["rc_guild_id"]


class LoggingCog(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):

        if message.guild.id != rc_guild_id:
            return

        author = message.author
        content = message.clean_content

        # format creation time in EST timezone.
        created_at = message.created_at
        est_time = created_at.astimezone(est)
        formatted_time = est_time.strftime("%Y-%m-%d %I:%M %p")

        attachments = message.attachments

        attachment_list = ""
        for attachment in attachments:
            attachment_list += f"{attachment.content_type} | {attachment.proxy_url}\n"

        embed = discord.Embed(
            color = discord.Color.orange(),
            description = f"**Message sent by {author.mention} deleted in <#{message.channel.id}>.**"
        )

        embed.set_author(name=author.name, icon_url=author.display_avatar)
        embed.add_field(name="Message ID", value=f"```\n{message.id}\n```", inline=False)
        embed.add_field(name="Content", value=f"```\n{content}\n```", inline=False)

        if attachments:
            embed.add_field(name="Attachments", value=attachment_list, inline=False)

        embed.set_footer(text=formatted_time)

        await message.guild.get_channel(logging_channel_id).send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):

        if after.guild.id != rc_guild_id:
            return

        author = after.author # same as before.author
        edit_time = datetime.now(est).strftime("%Y-%m-%d %I:%M %p")

        embed = discord.Embed(
            color = discord.Color.yellow(),
            description = f"**Message sent by {author.mention} edited in <#{after.channel.id}>.**"
        )

        embed.set_author(name=author.name, icon_url = author.display_avatar)
        embed.add_field(name="Message ID", value=f"```\n{after.id}\n```", inline=False)
        embed.add_field(name="Before", value=f"```\n{before.clean_content}\n```", inline=False)
        embed.add_field(name="After", value=f"```\n{after.clean_content}\n```", inline=False)
        embed.set_footer(text=edit_time)

        await after.guild.get_channel(logging_channel_id).send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):

        if guild.id != rc_guild_id:
            return

        current_time = datetime.now(est).strftime("%Y-%m-%d %I:%M %p")

        embed = discord.Embed(
            color = discord.Color.red(),
            title = f"**User @{user.name} was banned from the server.**"
        )
        embed.add_field(name="User ID", value=f"```\n{user.id}\n```")
        embed.set_thumbnail(url=user.display_avatar)
        embed.set_footer(text=current_time)

        await guild.get_channel(logging_channel_id).send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):

        if guild.id != rc_guild_id:
            return

        current_time = datetime.now(est).strftime("%Y-%m-%d %I:%M %p")

        embed = discord.Embed(
            color = discord.Color.red(),
            title = f"**User @{user.name} was unbanned from the server.**"
        )
        embed.add_field(name="User ID", value=f"```\n{user.id}\n```")
        embed.set_thumbnail(url=user.display_avatar)
        embed.set_footer(text=current_time)

        await guild.get_channel(logging_channel_id).send(embed=embed)




def setup(sbbot):
    sbbot.add_cog(LoggingCog(sbbot))
