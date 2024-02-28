import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

from services.Currency import Currency
from main import economy_config
from utils import economy_embeds, checks, interaction

load_dotenv('.env')

cash_balance_name = os.getenv("CASH_BALANCE_NAME")


class GamblingCog(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.slash_command(
        name="duel",
        description="Challenge another player to a fight.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def duel(self, ctx, *, opponent: discord.Option(discord.Member), bet: discord.Option(int)):
        challenger = ctx.author

        if challenger.id == opponent.id:
            return await ctx.respond(content="You cannot duel yourself.")
        elif opponent.bot:
            return await ctx.respond(content="You cannot duel a bot.")

        # Currency handler
        challenger_currency = Currency(ctx.author.id)
        opponent_currency = Currency(opponent.id)

        # check if challenger has enough cash
        challenger_cash_balance = challenger_currency.cash
        if bet > challenger_cash_balance or bet <= 0:
            return await ctx.respond(embed=economy_embeds.not_enough_cash())

        # if opponent doesn't have sufficient money, the bet will become the opponent's cash
        opponent_cash_balance = opponent_currency.cash
        all_in = ""
        if opponent_cash_balance <= 0:
            return await ctx.respond(f"Woops, you can't do that because **{opponent.name}** has no money.")
        elif bet > opponent_cash_balance:
            bet = opponent_cash_balance
            all_in = " | opponent's all-in"

        # challenge message
        view = interaction.DuelChallenge(opponent)

        await ctx.respond(
            content=f"**{challenger.name}** challenges {opponent.mention} to a duel ({cash_balance_name}{Currency.format(bet)}{all_in})\n"
                    f"Use the buttons to accept/deny (challenge expires after 60s)", view=view)
        await view.wait()

        if view.clickedConfirm:
            winner = random.choice([challenger, opponent])
            loser = opponent if winner == challenger else challenger
            combat_message = random.choice(economy_config["duel"]["combat_messages"]).format(f"**{winner.name}**",
                                                                                             f"**{loser.name}**")

            await ctx.respond(content=f"{combat_message}\n\n"
                                      f"{winner.mention} wins **{cash_balance_name}{Currency.format(bet)}**\n"
                                      f"{loser.mention} loses this bet.")

            # payouts
            if winner == challenger:
                challenger_currency.add_cash(bet)
                opponent_currency.take_cash(bet)

            elif winner == opponent:
                opponent_currency.add_cash(bet)
                challenger_currency.take_cash(bet)

        elif view.clickedDeny:
            await ctx.edit(content=f"**{opponent.name}** canceled the duel.")

        else:
            await ctx.edit(content=f"Time ran out.")

        challenger_currency.push()
        opponent_currency.push()


def setup(client):
    client.add_cog(GamblingCog(client))
