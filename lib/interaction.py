import discord
from discord.ui import View


class ExchangeConfirmation(View):
    def __init__(self, ctx):
        super().__init__(timeout=180)
        self.ctx = ctx
        self.clickedConfirm = False

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
            await self.message.edit(view=None)

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm_button_callback(self, button, interaction):
        await interaction.response.edit_message(view=None)
        self.clickedConfirm = True
        self.stop()

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.red)
    async def stop_button_callback(self, button, interaction):
        await interaction.response.edit_message(view=None)
        self.stop()

    async def interaction_check(self, interaction) -> bool:
        if interaction.user == self.ctx.author:
            return True
        await interaction.response.send_message(
            "You can't use these buttons, they're someone else's!",
            ephemeral=True,
        )
        return False
