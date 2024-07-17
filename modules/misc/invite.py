from discord import ButtonStyle
from discord.ext import bridge
from discord.ui import Button, View

from lib.constants import CONST
from lib.embed_builder import EmbedBuilder


async def cmd(ctx: bridge.BridgeContext) -> None:
    await ctx.respond(
        embed=EmbedBuilder.create_success_embed(
            ctx,
            description=CONST.STRINGS["invite_description"],
        ),
        view=InviteButton(),
    )


class InviteButton(View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        invite_button: Button = Button(
            label=CONST.STRINGS["invite_button_text"],
            style=ButtonStyle.url,
            url=CONST.INVITE_LINK,
        )
        self.add_item(invite_button)
