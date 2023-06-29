import discord
from discord.ext import commands

from data.Xp import Xp
from sb_tools import embeds, universal


class LevelingCog(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot

    @commands.slash_command(
        name="level",
        description="Displays your level and rank.",
        guild_only=True
    )
    @commands.check(universal.channel_check)
    async def level(self, ctx):
        xp_data = Xp(ctx.author.id)
        rank = xp_data.calculate_rank()
        needed_xp_for_next_level = Xp.xp_needed_for_next_level(xp_data.level)

        await ctx.respond(embed=embeds.level_command_message(ctx, xp_data.level, xp_data.xp,
                                                             needed_xp_for_next_level, rank))

    @commands.slash_command(
        name="leaderboard",
        description="Are ya winnin' son?",
        guild_only=True
    )
    @commands.check(universal.channel_check)
    async def leaderboard(self, ctx):
        leaderboard = Xp.load_leaderboard()

        embed = discord.Embed(
            color=0xadcca6
        )
        embed.set_author(name="Rave Cave Leaderboard",
                         icon_url="https://cdn.discordapp.com/icons/719227135151046699/"
                                  "49df8c284382af9dbcfd629c8eadc52c.webp?size=96")
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


def setup(sbbot):
    sbbot.add_cog(LevelingCog(sbbot))
