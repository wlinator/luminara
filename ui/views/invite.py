from discord import ButtonStyle
from discord.ui import Button, View
from lib.const import CONST


class InviteButton(View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        invite_button: Button = Button(
            label=CONST.STRINGS["invite_button_text"],
            style=ButtonStyle.url,
            url=CONST.INVITE_URL,
        )
        self.add_item(invite_button)