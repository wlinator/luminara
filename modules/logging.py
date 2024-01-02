import logging

from discord.ext import commands
import discord

from main import strings
from sb_tools import universal
import pytz
from datetime import datetime

racu_logs = logging.getLogger('Racu.Core')
est = pytz.timezone('US/Eastern')
logging_channel_id = 1191707328148418611


class LoggingCog(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
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
            color = discord.Color.red(),
            description = f"**Message sent by {author.mention} deleted in <#{message.channel.id}>.**"
        )

        embed.set_author(name=author.name, icon_url=author.display_avatar)
        embed.add_field(name="Message ID", value=f"```\n{message.id}\n```")
        embed.add_field(name="Content", value=f"```\n{content}\n```", inline=False)

        if attachments:
            embed.add_field(name="Attachments", value=attachment_list, inline=False)

        embed.set_footer(text=formatted_time)

        await message.guild.get_channel(logging_channel_id).send(embed=embed)


def setup(sbbot):
    sbbot.add_cog(LoggingCog(sbbot))
