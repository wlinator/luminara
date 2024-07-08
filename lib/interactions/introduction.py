import discord
from discord.ext import bridge
from discord.ui import View


class IntroductionStartButtons(View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.clickedStart = False
        self.clickedStop = False

    async def on_timeout(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True
        if self.message:
            await self.message.edit(view=None)

    @discord.ui.button(label="Start", style=discord.ButtonStyle.primary)
    async def short_button_callback(self, button, interaction):
        await interaction.response.edit_message(view=None)
        self.clickedStart = True
        self.stop()

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.red)
    async def stop_button_callback(self, button, interaction):
        await interaction.response.edit_message(view=None)
        self.clickedStop = True
        self.stop()


class IntroductionFinishButtons(View):
    def __init__(self, ctx: bridge.Context) -> None:
        """
        Initializes the IntroductionFinishConfirm view.
        """
        super().__init__(timeout=60)
        self.ctx = ctx
        self.clickedConfirm: bool = False

    async def on_timeout(self) -> None:
        """
        Called when the view times out. Disables all buttons and edits the message to remove the view.
        """
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True
        if self.message:
            await self.message.edit(view=None)

    @discord.ui.button(label="Post it!", style=discord.ButtonStyle.green)
    async def short_button_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ) -> None:
        await interaction.response.edit_message(view=None)
        self.clickedConfirm = True
        self.stop()

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.red)
    async def extended_button_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ) -> None:
        await interaction.response.edit_message(view=None)
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(
                "You can't use these buttons.", ephemeral=True
            )
            return False
        else:
            return True
