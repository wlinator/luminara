import discord

from services.xp_service import XpService


async def cmd(ctx):
    xp_data = XpService(ctx.author.id, ctx.guild.id)
    rank = xp_data.calculate_rank()
    needed_xp_for_next_level = XpService.xp_needed_for_next_level(xp_data.level)

    embed = discord.Embed(color=0xADCCA6, title=f"Level {xp_data.level}")
    embed.add_field(
        name="Progress to next level",
        value=XpService.generate_progress_bar(xp_data.xp, needed_xp_for_next_level),
        inline=False,
    )

    embed.set_footer(text=f"Server Rank: #{rank}")
    embed.set_thumbnail(url=ctx.author.display_avatar)

    await ctx.respond(embed=embed, content=ctx.author.mention)
