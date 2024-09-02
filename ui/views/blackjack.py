import discord
from discord.ext import commands
from discord.ui import Button, View

from lib.const import CONST


class BlackJackButtons(View):
    def __init__(self, ctx: commands.Context[commands.Bot]) -> None:
        super().__init__(timeout=180)
        self.ctx: commands.Context[commands.Bot] = ctx
        self.clickedHit: bool = False
        self.clickedStand: bool = False
        self.clickedDoubleDown: bool = False
        self.message: discord.Message | None = None

    async def on_timeout(self) -> None:
        self.children: list[discord.ui.Button[View]] = []

        for child in self.children:
            child.disabled = True

    @discord.ui.button(
        label=CONST.STRINGS["blackjack_hit"],
        style=discord.ButtonStyle.gray,
        emoji=CONST.BLACKJACK_HIT_EMOJI,
    )
    async def hit_button_callback(
        self,
        interaction: discord.Interaction,
        button: Button[View],
    ) -> None:
        self.clickedHit = True
        await interaction.response.defer()
        self.stop()

    @discord.ui.button(
        label=CONST.STRINGS["blackjack_stand"],
        style=discord.ButtonStyle.gray,
        emoji=CONST.BLACKJACK_STAND_EMOJI,
    )
    async def stand_button_callback(
        self,
        interaction: discord.Interaction,
        button: Button[View],
    ) -> None:
        self.clickedStand = True
        await interaction.response.defer()
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user == self.ctx.author:
            return True
        await interaction.response.send_message(
            CONST.STRINGS["error_cant_use_buttons"],
            ephemeral=True,
        )
        return False
