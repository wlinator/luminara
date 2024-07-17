import discord

from config.parser import JsonCache
from services.xp_service import XpRewardService

art = JsonCache.read_json("art")


async def show(ctx):
    level_reward = XpRewardService(ctx.guild.id)

    embed = discord.Embed(
        color=discord.Color.embed_background(),
        description="Read [the guide](https://wiki.wlinator.org/xprewards) before editing.\n",
    )

    icon = ctx.guild.icon if ctx.guild.icon else art["logo"]["opaque"]
    embed.set_author(name="Level Rewards", icon_url=icon)

    for level in sorted(level_reward.rewards.keys()):
        role_id, persistent = level_reward.rewards.get(level)
        role = ctx.guild.get_role(role_id)

        embed.description += (
            f"\n**Level {level}** -> {role.mention if role else 'Role not found'}"
        )

        if bool(persistent):
            embed.description += " (persistent)"

    await ctx.respond(embed=embed)


async def add_reward(ctx, level, role_id, persistent):
    level_reward = XpRewardService(ctx.guild.id)
    level_reward.add_reward(level, role_id, persistent)
    await show(ctx)


async def remove_reward(ctx, level):
    level_reward = XpRewardService(ctx.guild.id)
    level_reward.remove_reward(level)
    await show(ctx)
