import logging

import discord
from discord.ext import commands

from services.Currency import Currency
from services.Xp import Xp
from services.Dailies import Dailies
from lib import checks
from datetime import datetime, timedelta

logs = logging.getLogger('Racu.Core')


class LeaderboardV2Cog(commands.Cog):
    """
    A rewrite of the leaderboard command.
    This aims to show more information & a new "dailies" leaderboard.
    """

    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        name="leaderboard",
        description="Are ya winning' son?",
        guild_only=True
    )
    @commands.check(checks.channel)
    # @commands.cooldown(1, 180, commands.BucketType.user)
    async def leaderboard_v2(self, ctx):
        """
        Leaderboard command with a dropdown menu.
        :param ctx:
        """
        xp_lb = Xp.load_leaderboard()

        options = LeaderboardCommandOptions()
        view = LeaderboardCommandView(ctx, options)

        # default leaderboard
        embed = discord.Embed(
            color=discord.Color.embed_background(),
        )

        icon = ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
        embed.set_author(name="Level Leaderboard", icon_url=icon)
        embed.set_thumbnail(url="https://i.imgur.com/79XfsbS.png")

        value = ""
        for i, (user_id, xp, level, rank, xp_needed_for_next_level) in enumerate(xp_lb[:5], start=1):
            try:
                member = await ctx.guild.fetch_member(user_id)
                name = member.name

            except Exception as error:
                name = "Unknown User"
                logs.debug(f"Currency Leaderboard: Unknown User, {error}")

            embed.add_field(
                name=f"#{rank} - {name}",
                value=f"level: **{level}**\nxp: `{xp}/{xp_needed_for_next_level}`",
                inline=False
            )

        return await ctx.respond(embed=embed, view=view)


class LeaderboardCommandOptions(discord.ui.Select):
    """
    This class specifies the options for the leaderboard command:
    - XP
    - Currency
    - Daily streak
    """

    def __init__(self):
        super().__init__(
            placeholder="Select a leaderboard",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(
                    label="Levels",
                    description="See the top Rave Cave chatters!",
                    emoji="🆙",
                    value="xp"
                ),
                discord.SelectOption(
                    label="Currency",
                    description="Who is the richest Racu user?",
                    value="currency",
                    emoji="💸"
                ),
                discord.SelectOption(
                    label="Dailies",
                    description="See who has the biggest /daily streak!",
                    value="dailies",
                    emoji="📅"
                )
            ]
        )

    async def callback(self, interaction: discord.Interaction):
        await self.view.on_select(self.values[0], interaction)


class LeaderboardCommandView(discord.ui.View):
    """
    This view represents a dropdown menu to choose
    what kind of leaderboard to show.
    """

    def __init__(self, ctx, options: LeaderboardCommandOptions):
        self.ctx = ctx
        self.options = options

        super().__init__(timeout=180)
        self.add_item(self.options)

    async def on_timeout(self):
        await self.message.edit(view=None)
        #logs.info(f"[CommandHandler] /leaderboard command timed out - this is normal behavior.")
        self.stop()

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You can't use this menu, it's someone else's!", ephemeral=True)
            return False
        else:
            return True

    async def on_select(self, item, interaction):

        embed = discord.Embed(
            color=discord.Color.embed_background()
        )

        icon = self.ctx.guild.icon if self.ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"

        if interaction.data["values"][0] == "xp":
            xp_lb = Xp.load_leaderboard()
            embed.set_author(name="Level Leaderboard", icon_url=icon)
            embed.set_thumbnail(url="https://i.imgur.com/79XfsbS.png")

            value = ""
            for i, (user_id, xp, level, rank, xp_needed_for_next_level) in enumerate(xp_lb[:5], start=1):
                try:
                    member = await self.ctx.guild.fetch_member(user_id)
                    name = member.name

                except Exception as error:
                    name = "Unknown User"
                    logs.debug(f"Currency Leaderboard: Unknown User, {error}")

                embed.add_field(
                    name=f"#{rank} - {name}",
                    value=f"level: **{level}**\nxp: `{xp}/{xp_needed_for_next_level}`",
                    inline=False
                )

            await interaction.response.edit_message(embed=embed)

        elif interaction.data["values"][0] == "currency":
            cash_lb = Currency.load_leaderboard()
            embed.set_author(name="Currency Leaderboard", icon_url=icon)
            embed.set_thumbnail(url="https://i.imgur.com/wFsgSnr.png")

            value = ""
            for i, (user_id, balance, rank) in enumerate(cash_lb[:5], start=1):
                try:
                    member = await self.ctx.guild.fetch_member(user_id)
                    name = member.name

                except Exception as error:
                    name = "Unknown User"
                    logs.debug(f"Currency Leaderboard: Unknown User, {error}")

                embed.add_field(
                    name=f"#{rank} - {name}",
                    value=f"cash: **${Currency.format(balance)}**",
                    inline=False
                )

            await interaction.response.edit_message(embed=embed)

        elif interaction.data["values"][0] == "dailies":
            daily_lb = Dailies.load_leaderboard()
            embed.set_author(name="Daily Streak Leaderboard", icon_url=icon)
            embed.set_thumbnail(url="https://i.imgur.com/hSauh7K.png")

            for i, (user_id, streak, claimed_at, rank) in enumerate(daily_lb[:5], start=1):
                try:
                    member = await self.ctx.guild.fetch_member(user_id)
                    name = member.name

                except Exception as error:
                    name = "Unknown User"
                    logs.debug(f"Currency Leaderboard: Unknown User, {error}")

                claimed_at = datetime.fromisoformat(claimed_at)
                claimed_at = claimed_at.date()

                embed.add_field(
                    name=f"#{rank} - {name}",
                    value=f"highest streak: **{streak}**\nclaimed on: `{claimed_at}`",
                    inline=False
                )

            await interaction.response.edit_message(embed=embed)


def setup(client):
    client.add_cog(LeaderboardV2Cog(client))
