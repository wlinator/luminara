import asyncio
import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from data.Currency import Currency
from data.Inventory import Inventory
from data.Item import Item
from sb_tools import interaction, universal

racu_logs = logging.getLogger('Racu.Core')

load_dotenv('.env')
special_balance_name = os.getenv("SPECIAL_BALANCE_NAME")


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
        racu_logs.warning(f"{self.ctx.author.name}: /sell command timed out.")
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


class SellCog(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot

    @commands.slash_command(
        name="sell",
        description="Sell items from your inventory.",
        guild_only=True
    )
    @commands.check(universal.channel_check)
    async def sell(self, ctx):
        inv = Inventory(ctx.author.id)
        items = inv.get_sell_data()

        def response_check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        if not items:
            embed = discord.Embed(
                color=discord.Color.red(),
                description="You don't have any items to sell."
            )
            return await ctx.respond(embed=embed)

        options = SellCommandOptions(items)
        view = SellCommandView(ctx, options)

        embed = discord.Embed(
            color=discord.Color.embed_background(),
            description="Please select the item you want to sell."
        )
        await ctx.respond(embed=embed, view=view, content=ctx.author.mention)

        await view.wait()
        item = view.item

        if item:
            item = Item.get_item_by_display_name(view.item)
            quantity = item.get_quantity(ctx.author.id)
            amount_to_sell = 0

            if quantity == 1:
                embed = discord.Embed(
                    color=discord.Color.embed_background(),
                    description=f"You selected **{item.display_name}**, you have this item only once."
                )
                await ctx.edit(embed=embed)
                amount_to_sell = 1

            elif quantity > 1:
                embed = discord.Embed(
                    color=discord.Color.embed_background(),
                    description=f"You selected **{item.display_name}**, you have this item **{quantity}** times.\n"
                )
                embed.set_footer(text=f"Please type the amount you want to sell in this chat.")
                await ctx.edit(embed=embed)

                try:
                    amount_message = await self.bot.wait_for('message', check=response_check, timeout=60)
                    amount = amount_message.content

                    if is_number_between(amount, quantity):
                        amount_to_sell = int(amount)

                    else:
                        embed = discord.Embed(
                            color=discord.Color.red(),
                            description="Invalid input... try the command again."
                        )
                        return await ctx.respond(embed=embed, content=ctx.author.mention)

                except asyncio.TimeoutError:
                    await ctx.respond(
                        embed=discord.Embed(description="You ran out of time.", color=discord.Color.red()),
                        content=ctx.author.mention)
                    # racu_logs.warning(f"{ctx.author.id} Sell Timeout")
                    return

            else:
                embed = discord.Embed(
                    color=discord.Color.red(),
                    description="You dont have this item."
                )
                embed.set_footer(text="It shouldn't have showed up in the list, my apologies.")
                return await ctx.edit(embed=embed)

            """
            Item & amount selection finished.
            Get price, confirmation message & handle balances.
            """
            currency = Currency(ctx.author.id)
            worth = item.get_item_worth()
            total = worth * amount_to_sell
            view = interaction.ExchangeConfirmation(ctx)
            embed = discord.Embed(
                color=discord.Color.embed_background(),
                description=f"You're about to sell **{amount_to_sell} {item.display_name}(s)** for **${total}**. "
                            f"Are you absolutely sure about this?"
            )
            message = await ctx.respond(embed=embed, view=view, content=ctx.author.mention)
            await view.wait()

            if view.clickedConfirm:

                try:
                    currency.cash += total
                    currency.push()
                    inv.take_item(item, amount_to_sell)

                    embed = discord.Embed(
                        color=discord.Color.green(),
                        description=f"You have successfully sold "
                                    f"**{amount_to_sell} {item.display_name}(s)** for **${total}**."
                    )
                    await message.edit(embed=embed, view=None)

                except Exception as e:
                    await ctx.respond("Something went wrong, let Tess know about this.")
                    racu_logs.error(f"[CommandHandler] /sell post-confirmation error: {e}")
                    return

            else:
                return await message.edit(embed=None, content=f"**{ctx.author.name}** canceled the command.")

        else:
            embed = discord.Embed(
                color=discord.Color.red(),
                description="You selected not to sell anything."
            )
            await ctx.edit(embed=embed)


def setup(sbbot):
    sbbot.add_cog(SellCog(sbbot))
