from typing import Optional

import discord
from discord.ui import Button, View


class IntroductionStartButtons(View):
    def __init__(self, ctx) -> None:
        super().__init__(timeout=60)
        self.ctx = ctx
        self.clicked_start: bool = False
        self.clicked_stop: bool = False
        self.message: Optional[discord.Message] = None

    async def on_timeout(self) -> None:
        for child in self.children:
            if isinstance(child, Button):
                child.disabled = True
        if self.message:
            await self.message.edit(view=None)

    @discord.ui.button(label="Start", style=discord.ButtonStyle.primary)
    async def start_button_callback(
        self,
        interaction: discord.Interaction,
        button: Button,
    ) -> None:
        await interaction.response.edit_message(view=None)
        self.clicked_start = True
        self.stop()

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.red)
    async def stop_button_callback(
        self,
        interaction: discord.Interaction,
        button: Button,
    ) -> None:
        await interaction.response.edit_message(view=None)
        self.clicked_stop = True
        self.stop()


class IntroductionFinishButtons(View):
    def __init__(self, ctx) -> None:
        super().__init__(timeout=60)
        self.ctx = ctx
        self.clicked_confirm: bool = False
        self.message: Optional[discord.Message] = None

    async def on_timeout(self) -> None:
        for child in self.children:
            if isinstance(child, Button):
                child.disabled = True
        if self.message:
            await self.message.edit(view=None)

    @discord.ui.button(label="Post it!", style=discord.ButtonStyle.green)
    async def confirm_button_callback(
        self,
        interaction: discord.Interaction,
        button: Button,
    ) -> None:
        await interaction.response.edit_message(view=None)
        self.clicked_confirm = True
        self.stop()

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.red)
    async def stop_button_callback(
        self,
        interaction: discord.Interaction,
        button: Button,
    ) -> None:
        await interaction.response.edit_message(view=None)
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user == self.ctx.author:
            return True
        await interaction.response.send_message(
            "You can't use these buttons.",
            ephemeral=True,
        )
        return False
