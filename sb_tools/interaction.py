import discord
from discord.ui import View


class IntroButtons(View):
    def __init__(self, ctx):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.clickedShort = False
        self.clickedLong = False

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
            await self.message.edit(view=None)

    @discord.ui.button(label="Short", style=discord.ButtonStyle.primary)
    async def short_button_callback(self, button, interaction):
        await interaction.response.edit_message(view=None)
        self.clickedShort = True
        self.stop()

    @discord.ui.button(label="Extended", style=discord.ButtonStyle.green)
    async def extended_button_callback(self, button, interaction):
        await interaction.response.edit_message(view=None)
        self.clickedLong = True
        self.stop()

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.red)
    async def stop_button_callback(self, button, interaction):
        await interaction.response.edit_message(view=None)
        self.stop()

    # async def on_timeout(self):
    #     await self.ctx.

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You can't use these buttons, they're someone else's!",
                                                    ephemeral=True)
            return False
        else:
            return True


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

    @discord.ui.button(label="hit", style=discord.ButtonStyle.gray, emoji="<:hit:1119262723285467156> ")
    async def hit_button_callback(self, button, interaction):
        self.clickedHit = True
        await interaction.response.defer()
        self.stop()

    @discord.ui.button(label="stand", style=discord.ButtonStyle.gray, emoji="<:stand:1118923298298929154>")
    async def stand_button_callback(self, button, interaction):
        self.clickedStand = True
        await interaction.response.defer()
        self.stop()

    # @discord.ui.button(label="double down", style=discord.ButtonStyle.gray, emoji="<:double_down:1118923344549523656>")
    # async def double_down_button_callback(self):
    #     self.clickedDoubleDown = True
    #     self.stop()

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You can't use these buttons, they're someone else's!",
                                                    ephemeral=True)
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
            await interaction.response.send_message("You can't use these buttons, they're someone else's!",
                                                    ephemeral=True)
            return False
        else:
            return True


class Confirm(View):
    def __init__(self, ctx):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.clickedConfirm = False

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
            await self.message.edit(view=None)

    @discord.ui.button(label="Post it!", style=discord.ButtonStyle.green)
    async def short_button_callback(self, button, interaction):
        await interaction.response.edit_message(view=None)
        self.clickedConfirm = True
        self.stop()

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.red)
    async def extended_button_callback(self, button, interaction):
        await interaction.response.edit_message(view=None)
        self.stop()

    # async def on_timeout(self):
    #     await self.ctx.

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You can't use these buttons, they're someone else's!",
                                                    ephemeral=True)
            return False
        else:
            return True


class DuelChallenge(View):
    def __init__(self, opponent):
        super().__init__(timeout=60)
        self.opponent = opponent
        self.clickedConfirm = False
        self.clickedDeny = False

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
            await self.message.edit(view=None)

    @discord.ui.button(label="accept", style=discord.ButtonStyle.green)
    async def short_button_callback(self, button, interaction):
        await interaction.response.edit_message(view=None)
        self.clickedConfirm = True
        self.stop()

    @discord.ui.button(label="deny", style=discord.ButtonStyle.red)
    async def extended_button_callback(self, button, interaction):
        await interaction.response.edit_message(view=None)
        self.clickedDeny = True
        self.stop()

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.opponent:
            await interaction.response.send_message("You can't use these buttons, they're someone else's!",
                                                    ephemeral=True)
            return False
        else:
            return True

    @discord.ui.select(
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label="Choose a continent",
                default=True
            ),
            discord.SelectOption(
                label="Africa"
            ),
            discord.SelectOption(
                label="Europe"
            ),
            discord.SelectOption(
                label="Asia"
            ),
            discord.SelectOption(
                label="North America"
            ),
            discord.SelectOption(
                label="South America"
            ),
            discord.SelectOption(
                label="Oceania"
            )
        ]
    )
    async def select_callback(self, select, interaction):
        self.location = select.values[0]
        await interaction.response.edit_message(view=None)
        self.stop()
