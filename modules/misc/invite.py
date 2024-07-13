import discord
from discord.ui import View

from lib.embed_builder import EmbedBuilder
from lib.constants import CONST


async def cmd(ctx):
    await ctx.respond(
        embed=EmbedBuilder.create_success_embed(
            ctx, description=CONST.STRINGS["invite_description"]
        ),
        view=InviteButton(),
    )


class InviteButton(View):
    def __init__(self):
        super().__init__(timeout=None)
        invite_button = discord.ui.Button(
            label=CONST.STRINGS["invite_button_text"],
            style=discord.ButtonStyle.url,
            url=CONST.INVITE_LINK,
        )
        self.add_item(invite_button)
