import discord

from services.level_reward import LevelReward
from config.parser import JsonCache

art = JsonCache.read_json("art")


async def show(ctx):
    level_reward = LevelReward(ctx.guild.id)

    embed = discord.Embed(
        color=discord.Color.embed_background(),
        description="[Read the guide before editing](https://gitlab.com/wlinator/Racu/wikis/Role-Rewards).\n"
    )

    icon = ctx.guild.icon if ctx.guild.icon else art["logo"]["opaque"]
    embed.set_author(name="Level Rewards", icon_url=icon)

    for level in sorted(sorted(level_reward.rewards.keys())):
        role_id, persistent = level_reward.rewards.get(level)
        role = ctx.guild.get_role(role_id)

        embed.description += f"\n**Level {level}** -> {role.mention}"

        if bool(persistent):
            embed.description += " (persistent)"

    await ctx.respond(embed=embed)


async def add_reward(ctx, level, role_id, persistent):
    level_reward = LevelReward(ctx.guild.id)

    if len(level_reward.rewards) >= 10:
        raise discord.BadArgument("a server can't have more than 10 XP rewards.")

    level_reward.add_reward(level, role_id, persistent)
    await show(ctx)


async def remove_reward(ctx, level):
    level_reward = LevelReward(ctx.guild.id)
    level_reward.remove_reward(level)
    await show(ctx)

