from datetime import datetime

import discord
from discord.ext import bridge

from lib.constants import CONST
from lib.embed_builder import EmbedBuilder
from services.currency_service import Currency
from services.daily_service import Dailies
from services.xp_service import XpService


async def cmd(ctx: bridge.Context) -> None:
    if not ctx.guild:
        return

    options = LeaderboardCommandOptions()
    view = LeaderboardCommandView(ctx, options)

    # default leaderboard
    embed = EmbedBuilder.create_success_embed(
        ctx=ctx,
        thumbnail_url=CONST.FLOWERS_ART,
        show_name=False,
    )

    icon = ctx.guild.icon.url if ctx.guild.icon else CONST.FLOWERS_ART
    await view.populate_leaderboard("xp", embed, icon)

    await ctx.respond(embed=embed, view=view)


class LeaderboardCommandOptions(discord.ui.Select):
    """
    This class specifies the options for the leaderboard command:
    - XP
    - Currency
    - Daily streak
    """

    def __init__(self) -> None:
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

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.view:
            await self.view.on_select(self.values[0], interaction)


class LeaderboardCommandView(discord.ui.View):
    """
    This view represents a dropdown menu to choose
    what kind of leaderboard to show.
    """

    def __init__(self, ctx: bridge.Context, options: LeaderboardCommandOptions) -> None:
        self.ctx = ctx
        self.options = options

        super().__init__(timeout=180)
        self.add_item(self.options)

    async def on_timeout(self) -> None:
        if self.message:
            await self.message.edit(view=None)
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user and interaction.user != self.ctx.author:
            embed = EmbedBuilder.create_error_embed(
                ctx=self.ctx,
                author_text=interaction.user.name,
                description=CONST.STRINGS["xp_lb_cant_use_dropdown"],
                show_name=False,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        return True

    async def on_select(self, item: str, interaction: discord.Interaction) -> None:
        if not self.ctx.guild:
            return

        embed = EmbedBuilder.create_success_embed(
            ctx=self.ctx,
            thumbnail_url=CONST.FLOWERS_ART,
            show_name=False,
        )

        icon = self.ctx.guild.icon.url if self.ctx.guild.icon else CONST.FLOWERS_ART

        await self.populate_leaderboard(item, embed, icon)

        await interaction.response.edit_message(embed=embed)

    async def populate_leaderboard(self, item: str, embed, icon):
        leaderboard_methods = {
            "xp": self._populate_xp_leaderboard,
            "currency": self._populate_currency_leaderboard,
            "dailies": self._populate_dailies_leaderboard,
        }
        await leaderboard_methods[item](embed, icon)

    async def _populate_xp_leaderboard(self, embed, icon):
        if not self.ctx.guild:
            return

        xp_lb = XpService.load_leaderboard(self.ctx.guild.id)
        embed.set_author(name=CONST.STRINGS["xp_lb_author"], icon_url=icon)

        for rank, (user_id, xp, level, xp_needed_for_next_level) in enumerate(
            xp_lb[:5],
            start=1,
        ):
            try:
                member = await self.ctx.guild.fetch_member(user_id)
            except discord.HTTPException:
                continue  # skip user if not in guild

            embed.add_field(
                name=CONST.STRINGS["xp_lb_field_name"].format(rank, member.name),
                value=CONST.STRINGS["xp_lb_field_value"].format(
                    level,
                    xp,
                    xp_needed_for_next_level,
                ),
                inline=False,
            )

    async def _populate_currency_leaderboard(self, embed, icon):
        if not self.ctx.guild:
            return

        cash_lb = Currency.load_leaderboard()
        embed.set_author(name=CONST.STRINGS["xp_lb_currency_author"], icon_url=icon)
        embed.set_thumbnail(url=CONST.TEAPOT_ART)

        for user_id, balance, rank in cash_lb[:5]:
            try:
                member = await self.ctx.guild.fetch_member(user_id)
            except discord.HTTPException:
                member = None

            name = member.name if member else str(user_id)

            embed.add_field(
                name=f"#{rank} - {name}",
                value=CONST.STRINGS["xp_lb_currency_field_value"].format(
                    Currency.format(balance),
                ),
                inline=False,
            )

    async def _populate_dailies_leaderboard(self, embed, icon):
        if not self.ctx.guild:
            return

        daily_lb = Dailies.load_leaderboard()
        embed.set_author(name=CONST.STRINGS["xp_lb_dailies_author"], icon_url=icon)
        embed.set_thumbnail(url=CONST.MUFFIN_ART)

        for user_id, streak, claimed_at, rank in daily_lb[:5]:
            try:
                member = await self.ctx.guild.fetch_member(user_id)
            except discord.HTTPException:
                member = None

            name = member.name if member else user_id

            claimed_at = datetime.fromisoformat(claimed_at).date()

            embed.add_field(
                name=f"#{rank} - {name}",
                value=CONST.STRINGS["xp_lb_dailies_field_value"].format(
                    streak,
                    claimed_at,
                ),
                inline=False,
            )
