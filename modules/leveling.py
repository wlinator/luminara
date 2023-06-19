import time

from discord.ext import commands

from data.Currency import Currency
from data.Xp import Xp
from sb_tools import embeds, universal, level_messages, reactions, xp_functions


class Leveling(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        await reactions.check_for_reaction(message)

        user_id = message.author.id
        current_time = time.time()
        xp_data = Xp.get_user_xp_data(user_id)
        (current_xp, current_level, cooldown) = xp_data[0]

        if cooldown and current_time < cooldown:
            print(f"XP UPDATE --- {message.author.name} sent a message but is on XP cooldown.")
            return

        gain_data = Xp.load_gain_data()
        xp_gain = gain_data[0]
        cooldown = gain_data[1]

        new_xp = current_xp + xp_gain
        needed_xp_for_next_level = xp_functions.xp_needed_for_next_level(current_level)

        if new_xp >= needed_xp_for_next_level:
            # new level was reached
            new_level = current_level + 1
            new_xp = 0

            Xp.update_user_xp(user_id, new_xp, new_level, current_time + cooldown)
            print(f"XP UPDATE --- {message.author.name} leveled up; new_level = {new_level}.")
            await message.channel.send(content=f"<@{user_id}> {level_messages.load_level_message(new_level)}")

            # assign level role if necessary:
            if new_level in [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]:
                await Xp.assign_level_role(message.author, new_level)

            # Currency handler
            user_currency = Currency(user_id)

            # award a special_balance_currency
            amount = 1
            user_currency.add_special(amount)
            user_currency.push()

        else:
            # user gained XP but not new level
            Xp.update_user_xp(user_id, new_xp, current_level, current_time + cooldown)
            print(f"XP UPDATE --- {message.author.name} gained {xp_gain} XP; new_xp = {new_xp}.")

        """
        Level calculation
        Linear = 9x + 27
        """

    @commands.slash_command(
        name="level",
        description="Displays your level and rank.",
        guild_only=True
    )
    @commands.check(universal.channel_check)
    async def level(self, ctx):
        xp_data = Xp.get_user_xp_data(ctx.author.id)
        (current_xp, current_level, cooldown) = xp_data[0]
        rank = Xp.calculate_rank(ctx.author.id)
        needed_xp_for_next_level = xp_functions.xp_needed_for_next_level(current_level)

        await ctx.respond(embed=embeds.level_command_message(ctx, current_level, current_xp,
                                                             needed_xp_for_next_level, rank))

    @commands.slash_command(
        name="leaderboard",
        description="Are ya winnin' son?",
        guild_only=True
    )
    @commands.check(universal.channel_check)
    async def leaderboard(self, ctx):
        leaderboard = Xp.load_leaderboard()
        embed = await embeds.leaderboard_message(ctx, leaderboard)
        await ctx.respond(embed=embed)


def setup(sbbot):
    sbbot.add_cog(Leveling(sbbot))
