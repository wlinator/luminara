from datetime import datetime

import discord

from lib.embed_builder import EmbedBuilder
from services.currency_service import Currency
from services.daily_service import Dailies
from services.xp_service import XpService


async def cmd(ctx):
    xp_lb = XpService.load_leaderboard(ctx.guild.id)

    options = LeaderboardCommandOptions()
    view = LeaderboardCommandView(ctx, options)

    # default leaderboard
    embed = EmbedBuilder.create_success_embed(
        ctx=ctx,
        title="Level Leaderboard",
        thumbnail_url="https://i.imgur.com/79XfsbS.png",
        show_name=False,
    )

    icon = ctx.guild.icon.url if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
    embed.set_author(name="Level Leaderboard", icon_url=icon)

    rank = 1
    for user_id, xp, level, xp_needed_for_next_level in xp_lb[:5]:
        try:
            member = await ctx.guild.fetch_member(user_id)
        except discord.HTTPException:
            continue  # skip user if not in guild

        embed.add_field(
            name=f"#{rank} - {member.name}",
            value=f"level: **{level}**\nxp: `{xp}/{xp_needed_for_next_level}`",
            inline=False,
        )

        rank += 1

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
                    description="See the top chatters of this server!",
                    emoji="🆙",
                    value="xp",
                ),
                discord.SelectOption(
                    label="Currency",
                    description="Who is the richest Lumi user?",
                    value="currency",
                    emoji="💸",
                ),
                discord.SelectOption(
                    label="Dailies",
                    description="See who has the biggest streak!",
                    value="dailies",
                    emoji="📅",
                ),
            ],
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
        # logs.info(f"[CommandHandler] /leaderboard command timed out - this is normal behavior.")
        self.stop()

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(
                "You can't use this menu, it's someone else's!", ephemeral=True
            )
            return False
        else:
            return True

    async def on_select(self, item, interaction):
        embed = EmbedBuilder.create_success_embed(
            ctx=self.ctx,
            title="",
            thumbnail_url="https://i.imgur.com/79XfsbS.png",
            show_name=False,
        )

        icon = (
            self.ctx.guild.icon.url
            if self.ctx.guild.icon
            else "https://i.imgur.com/79XfsbS.png"
        )

        if item == "xp":
            xp_lb = XpService.load_leaderboard(self.ctx.guild.id)
            embed.set_author(name="Level Leaderboard", icon_url=icon)

            rank = 1
            for user_id, xp, level, xp_needed_for_next_level in xp_lb[:5]:
                try:
                    member = await self.ctx.guild.fetch_member(user_id)
                except discord.HTTPException:
                    continue  # skip user if not in guild

                embed.add_field(
                    name=f"#{rank} - {member.name}",
                    value=f"level: **{level}**\nxp: `{xp}/{xp_needed_for_next_level}`",
                    inline=False,
                )

                rank += 1

        elif item == "currency":
            cash_lb = Currency.load_leaderboard()
            embed.set_author(name="Currency Leaderboard", icon_url=icon)
            embed.set_thumbnail(url="https://i.imgur.com/wFsgSnr.png")

            for user_id, balance, rank in cash_lb[:5]:
                try:
                    member = await self.ctx.guild.fetch_member(user_id)
                except discord.HTTPException:
                    member = None

                name = member.name if member else str(user_id)

                embed.add_field(
                    name=f"#{rank} - {name}",
                    value=f"cash: **${Currency.format(balance)}**",
                    inline=False,
                )

        elif item == "dailies":
            daily_lb = Dailies.load_leaderboard()
            embed.set_author(name="Daily Streak Leaderboard", icon_url=icon)
            embed.set_thumbnail(url="https://i.imgur.com/hSauh7K.png")

            for user_id, streak, claimed_at, rank in daily_lb[:5]:
                try:
                    member = await self.ctx.guild.fetch_member(user_id)
                except discord.HTTPException:
                    member = None

                name = member.name if member else user_id

                claimed_at = datetime.fromisoformat(claimed_at).date()

                embed.add_field(
                    name=f"#{rank} - {name}",
                    value=f"highest streak: **{streak}**\nclaimed on: `{claimed_at}`",
                    inline=False,
                )

        await interaction.response.edit_message(embed=embed)
