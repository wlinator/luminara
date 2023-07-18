import logging

import discord
from discord.ext import commands

from data.Currency import Currency
from data.Xp import Xp
from sb_tools import universal

racu_logs = logging.getLogger('Racu.Core')


class LeaderboardCog(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot

    @commands.slash_command(
        name="leaderboard",
        description="Are ya winning' son?",
        guild_only=True
    )
    @commands.check(universal.channel_check)
    @commands.cooldown(1, 180, commands.BucketType.user)
    async def leaderboard(self, ctx):
        xp_lb = Xp.load_leaderboard()
        cash_lb = Currency.load_leaderboard()

        embed = discord.Embed(
            color=discord.Color.embed_background(),
        )

        icon = ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"

        embed.set_author(name="Rave Cave Leaderboard", icon_url=icon)
        embed.set_thumbnail(url="https://i.imgur.com/79XfsbS.png")
        embed.set_footer(text=f"Do /level to see your rank.")

        # XP FIELD
        value = ""
        for i, (user_id, xp, level, rank, xp_needed_for_next_level) in enumerate(xp_lb[:5], start=1):
            try:
                member = await ctx.guild.fetch_member(user_id)
                name = member.name

            except Exception as error:
                name = "Unknown User"
                racu_logs.debug(f"Currency Leaderboard: Unknown User, {error}")

            value += f"Lv. {level} - {name}\n"

        embed.add_field(
            name="Top Five Chatters",
            value=value,
            inline=False
        )

        # CURRENCY FIELD
        value = ""
        for i, (user_id, cash_balance, rank) in enumerate(cash_lb[:5], start=1):
            try:
                member = await ctx.guild.fetch_member(user_id)
                name = member.name

            except Exception as error:
                name = "Unknown User"
                racu_logs.debug(f"Currency Leaderboard: Unknown User, {error}")

            value += f"${Currency.format_human(cash_balance)} - {name}\n"

        embed.add_field(
            name=f"Top Five Wealth",
            value=value,
            inline=False
        )

        await ctx.respond(embed=embed)


def setup(sbbot):
    sbbot.add_cog(LeaderboardCog(sbbot))
