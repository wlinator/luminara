import locale
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
        name="leaderboardv2",
        description="Are ya winning' son?",
        guild_only=True
    )
    @commands.check(universal.beta_check)
    async def leaderboardv2(self, ctx):
        xp_lb = Xp.load_leaderboard()
        cash_lb = Currency.load_leaderboard()

        embed = discord.Embed(
            color=discord.Color.embed_background(),
        )
        embed.set_author(name="Rave Cave Leaderboard")
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

            locale.setlocale(locale.LC_ALL, '')
            cash_balance = locale.format_string("%d", cash_balance, grouping=True)

            value += f"${cash_balance} - {name}\n"

        embed.add_field(
            name=f"Top Five Wealth",
            value=value,
            inline=False
        )

        await ctx.respond(embed=embed)

    @commands.slash_command(
        name="leaderboard",
        description="Are ya winnin' son?",
        guild_only=True
    )
    @commands.check(universal.channel_check)
    async def leaderboard(self, ctx, *, type: discord.Option(choices=["levels", "currency"])):

        if type == "levels":
            leaderboard = Xp.load_leaderboard()

            embed = discord.Embed(
                color=0xadcca6
            )
            embed.set_author(name="XP Leaderboard")
            embed.set_footer(text=f"Do /level to see your rank.")
            embed.set_thumbnail(url="https://i.imgur.com/79XfsbS.png")
            for i, (user_id, xp, level, rank, xp_needed_for_next_level) in enumerate(leaderboard[:5], start=1):
                try:
                    member = await ctx.guild.fetch_member(user_id)
                    name = member.name
                except:
                    name = "Unknown User"

                embed.add_field(
                    name=f"#{rank} - {name}",
                    value=f"level: `{level}`\nxp: `{xp}/{xp_needed_for_next_level}`",
                    inline=False
                )

            await ctx.respond(embed=embed)

        elif type == "currency":
            leaderboard = Currency.load_leaderboard()

            embed = discord.Embed(
                color=discord.Color.embed_background()
            )
            embed.set_author(name="Currency Leaderboard")
            embed.set_footer(text="Start earning money with /daily!")
            embed.set_thumbnail(url="https://i.imgur.com/wFsgSnr.png")

            for i, (user_id, cash_balance, rank) in enumerate(leaderboard[:10], start=1):
                try:
                    member = await ctx.guild.fetch_member(user_id)
                    name = member.name

                except Exception as error:
                    name = "Unknown User"
                    racu_logs.debug(f"Currency Leaderboard: Unknown User, {error}")

                locale.setlocale(locale.LC_ALL, '')
                cash_balance = locale.format_string("%d", cash_balance, grouping=True)

                embed.add_field(
                    name=f"${cash_balance} - {name}",
                    value="",
                    inline=False
                )

            await ctx.respond(embed=embed)


def setup(sbbot):
    sbbot.add_cog(LeaderboardCog(sbbot))
