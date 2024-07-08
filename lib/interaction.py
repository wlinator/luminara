import discord
from discord.ext import commands
from discord.ui import View


class BlackJackButtons(View):
    def __init__(self, ctx):
        super().__init__(timeout=180)
        self.ctx = ctx
        self.clickedHit = False
        self.clickedStand = False
        self.clickedDoubleDown = False

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
            await self.message.edit(view=None)

    @discord.ui.button(
        label="hit", style=discord.ButtonStyle.gray, emoji="<:hit:1119262723285467156> "
    )
    async def hit_button_callback(self, button, interaction):
        self.clickedHit = True
        await interaction.response.defer()
        self.stop()

    @discord.ui.button(
        label="stand",
        style=discord.ButtonStyle.gray,
        emoji="<:stand:1118923298298929154>",
    )
    async def stand_button_callback(self, button, interaction):
        self.clickedStand = True
        await interaction.response.defer()
        self.stop()

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(
                "You can't use these buttons, they're someone else's!", ephemeral=True
            )
            return False
        else:
            return True


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
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(
                "You can't use these buttons, they're someone else's!", ephemeral=True
            )
            return False
        else:
            return True
