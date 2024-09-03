import contextlib
from datetime import datetime

import discord
from discord.ext import commands

from lib.client import Luminara
from lib.const import CONST
from services.currency_service import Currency
from services.daily_service import Dailies
from services.xp_service import XpService
from ui.embeds import Builder


class LeaderboardCommandOptions(discord.ui.Select[discord.ui.View]):
    """
    This class specifies the options for the leaderboard command:
    - XP
    - Currency
    - Daily streak
    """

    def __init__(self) -> None:
        options: list[discord.SelectOption] = [
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
        ]
        super().__init__(
            placeholder="Select a leaderboard",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        if isinstance(self.view, LeaderboardCommandView):
            await self.view.on_select(self.values[0], interaction)


class LeaderboardCommandView(discord.ui.View):
    """
    This view represents a dropdown menu to choose
    what kind of leaderboard to show.
    """

    ctx: commands.Context[Luminara]
    options: LeaderboardCommandOptions

    def __init__(
        self,
        ctx: commands.Context[Luminara],
        options: LeaderboardCommandOptions,
    ) -> None:
        super().__init__(timeout=180)
        self.ctx = ctx
        self.options = options
        self.add_item(self.options)

    async def on_timeout(self) -> None:
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user and interaction.user != self.ctx.author:
            embed = Builder.create_embed(
                theme="error",
                user_name=interaction.user.name,
                description=CONST.STRINGS["xp_lb_cant_use_dropdown"],
                hide_name_in_description=True,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        return True

    async def on_select(self, item: str, interaction: discord.Interaction) -> None:
        if not self.ctx.guild:
            return

        embed = Builder.create_embed(
            theme="success",
            user_name=interaction.user.name,
            thumbnail_url=CONST.FLOWERS_ART,
            hide_name_in_description=True,
        )

        icon = self.ctx.guild.icon.url if self.ctx.guild.icon else CONST.FLOWERS_ART

        await self.populate_leaderboard(item, embed, icon)

        await interaction.response.edit_message(embed=embed)

    async def populate_leaderboard(
        self,
        item: str,
        embed: discord.Embed,
        icon: str,
    ) -> None:
        leaderboard_methods = {
            "xp": self._populate_xp_leaderboard,
            "currency": self._populate_currency_leaderboard,
            "dailies": self._populate_dailies_leaderboard,
        }
        await leaderboard_methods[item](embed, icon)

    async def _populate_xp_leaderboard(self, embed: discord.Embed, icon: str) -> None:
        if not self.ctx.guild:
            return

        xp_lb: list[tuple[int, int, int, int]] = XpService.load_leaderboard(
            self.ctx.guild.id,
        )
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

    async def _populate_currency_leaderboard(
        self,
        embed: discord.Embed,
        icon: str,
    ) -> None:
        if not self.ctx.guild:
            return

        cash_lb: list[tuple[int, int, int]] = Currency.load_leaderboard()
        embed.set_author(name=CONST.STRINGS["xp_lb_currency_author"], icon_url=icon)
        embed.set_thumbnail(url=CONST.TEAPOT_ART)

        for user_id, balance, rank in cash_lb[:5]:
            member: discord.Member | None = None
            with contextlib.suppress(discord.HTTPException):
                member = await self.ctx.guild.fetch_member(user_id)
            name = member.name if member else str(user_id)

            embed.add_field(
                name=f"#{rank} - {name}",
                value=CONST.STRINGS["xp_lb_currency_field_value"].format(
                    Currency.format(balance),
                ),
                inline=False,
            )

    async def _populate_dailies_leaderboard(
        self,
        embed: discord.Embed,
        icon: str,
    ) -> None:
        if not self.ctx.guild:
            return

        daily_lb: list[tuple[int, int, str, int]] = Dailies.load_leaderboard()
        embed.set_author(name=CONST.STRINGS["xp_lb_dailies_author"], icon_url=icon)
        embed.set_thumbnail(url=CONST.MUFFIN_ART)

        for user_id, streak, claimed_at, rank in daily_lb[:5]:
            member: discord.Member | None = None
            with contextlib.suppress(discord.HTTPException):
                member = await self.ctx.guild.fetch_member(user_id)
            name = member.name if member else str(user_id)

            claimed_at_date = datetime.fromisoformat(claimed_at).date()

            embed.add_field(
                name=f"#{rank} - {name}",
                value=CONST.STRINGS["xp_lb_dailies_field_value"].format(
                    streak,
                    claimed_at_date,
                ),
                inline=False,
            )
