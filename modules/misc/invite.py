import logging

import discord
from discord.ui import View

from lib.embeds.info import MiscInfo

logs = logging.getLogger('Lumi.Core')
url = "https://discord.com/oauth2/authorize?client_id=1038050427272429588&permissions=8&scope=bot"


async def cmd(ctx):
    embed = MiscInfo.invite(ctx)
    view = InviteButton()

    await ctx.respond(embed=embed, view=view)


class InviteButton(View):
    def __init__(self):
        super().__init__(timeout=None)
        invite_button = discord.ui.Button(label="Invite Lumi", style=discord.ButtonStyle.url, url=url)
        self.add_item(invite_button)
