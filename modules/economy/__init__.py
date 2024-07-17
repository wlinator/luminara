import discord
from discord.ext import commands, bridge

from lib import checks
from modules.economy import blackjack, slots, balance, give, daily


class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @bridge.bridge_command(
        name="balance",
        aliases=["bal", "$"],
        description="Shows your current Lumi balance.",
        help="Shows your current Lumi balance. The economy system is global, meaning your balance will be synced in "
        "all servers.",
        guild_only=True,
    )
    @commands.guild_only()
    @checks.allowed_in_channel()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def balance_command(self, ctx):
        return await balance.cmd(ctx)

    @bridge.bridge_command(
        name="blackjack",
        aliases=["bj"],
        description="Start a game of blackjack.",
        help="Start a game of blackjack.",
        guild_only=True,
    )
    @commands.guild_only()
    @checks.allowed_in_channel()
    async def blackjack_command(self, ctx, *, bet: int):
        return await blackjack.cmd(ctx, bet)

    @bridge.bridge_command(
        name="daily",
        aliases=["timely"],
        description="Claim your daily reward.",
        help="Claim your daily reward! Reset is at 7 AM EST.",
        guild_only=True,
    )
    @commands.guild_only()
    @checks.allowed_in_channel()
    async def daily_command(self, ctx):
        return await daily.cmd(ctx)

    @commands.slash_command(
        name="give", description="Give a server member some cash.", guild_only=True
    )
    @commands.guild_only()
    @checks.allowed_in_channel()
    async def give_command(self, ctx, *, user: discord.Member, amount: int):
        return await give.cmd(ctx, user, amount)

    @commands.command(
        name="give",
        help="Give a server member some cash. You can use ID or mention them.",
    )
    @commands.guild_only()
    @checks.allowed_in_channel()
    async def give_command_prefixed(self, ctx, user: discord.User, *, amount: int):
        try:
            member = await ctx.guild.fetch_member(user.id)
        except discord.HTTPException:
            raise commands.BadArgument("I couldn't find that user in this server.")

        return await give.cmd(ctx, member, amount)

    @bridge.bridge_command(
        name="slots",
        aliases=["slot"],
        description="Start a slots game.",
        help="Spin the slots for a chance to win the jackpot!",
        guild_only=True,
    )
    @commands.guild_only()
    @checks.allowed_in_channel()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slots_command(self, ctx, *, bet: int):
        return await slots.cmd(self, ctx, bet)


def setup(client):
    client.add_cog(Economy(client))
