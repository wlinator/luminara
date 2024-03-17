import logging

import discord
from dotenv import load_dotenv

logs = logging.getLogger('Racu.Core')

load_dotenv('.env')


class SellCommandOptions(discord.ui.Select):
    def __init__(self, items: str):
        self.item = None

        super().__init__(
            placeholder="Select an item",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(label=item) for item in items
            ]
        )

    async def callback(self, interaction: discord.Interaction):
        await self.view.on_select(self.values[0], interaction)


class SellCommandView(discord.ui.View):
    def __init__(self, ctx, options: SellCommandOptions):
        self.ctx = ctx
        self.options = options
        self.item = None

        super().__init__(timeout=60)
        self.add_item(self.options)

    async def on_timeout(self):
        embed = discord.Embed(
            color=discord.Color.red(),
            description="You ran out of time."
        )
        await self.message.edit(embed=embed, view=None)
        logs.warning(f"{self.ctx.author.name}: /sell command timed out.")
        self.stop()

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You can't use this menu, it's someone else's!", ephemeral=True)
            return False
        else:
            return True

    async def on_select(self, item, interaction):
        self.item = item
        await interaction.response.edit_message(view=None)
        self.stop()


def is_number_between(value, upper_limit):
    try:
        # Convert the value to an integer
        number = int(value)

        # Check if the number is between 1 and the upper limit
        if 1 <= number <= upper_limit:
            return True

    except ValueError:
        pass

    return False
