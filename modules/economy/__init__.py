import discord
from discord.ext import commands, bridge

from lib import checks
from lib.embeds.error import EconErrors, GenericErrors
from modules.economy import blackjack, sell, slots, balance, stats, give, inventory, daily


class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client

    @bridge.bridge_command(
        name="balance",
        aliases=["bal", "$"],
        description="See how much cash you have.",
        help="Shows your current Racu balance. The economy system is global, meaning your balance will be the same in "
             "all servers.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def balance_command(self, ctx):
        return await balance.cmd(ctx)

    @balance_command.error
    async def on_command_error(self, ctx, error):
        await ctx.respond(embed=GenericErrors.default_exception(ctx))
        raise error

    @bridge.bridge_command(
        name="blackjack",
        aliases=["bj"],
        description="Start a game of blackjack.",
        help="Start a game of blackjack.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def blackjack_command(self, ctx, *, bet: int):
        return await blackjack.cmd(ctx, bet)

    @blackjack_command.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.respond(embed=EconErrors.missing_bet(ctx))
        elif isinstance(error, commands.BadArgument):
            await ctx.respond(embed=EconErrors.bad_bet_argument(ctx))
        else:
            await ctx.respond(embed=GenericErrors.default_exception(ctx))
            raise error

    @bridge.bridge_command(
        name="daily",
        aliases=["timely"],
        description="Claim your daily cash!",
        help="Claim your daily reward! The daily reset is at 7 AM EST.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def daily_command(self, ctx):
        return await daily.cmd(ctx)

    @daily_command.error
    async def on_command_error(self, ctx, error):
        await ctx.respond(embed=GenericErrors.default_exception(ctx))
        raise error

    @commands.slash_command(
        name="give",
        description="Give another user some currency.",
        help="Give another server member some cash.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def give_command(self, ctx, *, user: discord.Member, amount: int):
        return await give.cmd(ctx, user, amount)

    @give_command.error
    async def on_command_error(self, ctx, error):
        await ctx.respond(embed=GenericErrors.default_exception(ctx))
        raise error

    @commands.command(
        name="give",
        help="Give another user some cash. You can use someone's user ID or mention someone. The user has to be in the "
             "guild you invoke this command in."
    )
    async def give_command_prefixed(self, ctx, user: discord.User, *, amount: int):

        try:
            member = await ctx.guild.fetch_member(user.id)
        except discord.HTTPException:
            raise commands.BadArgument

        return await give.cmd(ctx, member, amount)

    @give_command_prefixed.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.respond(embed=EconErrors.missing_argument(ctx))
        elif isinstance(error, commands.BadArgument):
            await ctx.respond(embed=EconErrors.bad_argument(ctx))
        else:
            await ctx.respond(embed=GenericErrors.default_exception(ctx))
            raise error

    @bridge.bridge_command(
        name="inventory",
        aliases=["inv"],
        description="Display your inventory.",
        help="Display your inventory, this will also show your Racu badges if you have any.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def inventory(self, ctx):
        return await inventory.cmd(self, ctx)

    @bridge.bridge_command(
        name="sell",
        description="Sell items from your inventory.",
        help="Sell something from your inventory. This command has no arguments because when you do the command "
             "it will lead you through the process of selling items.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def sell_command(self, ctx):
        return await sell.cmd(self, ctx)

    @bridge.bridge_command(
        name="slots",
        aliases=["slot"],
        descriptions="Spin the slots for a chance to win the jackpot!",
        help="Starts a slots game.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def slots_command(self, ctx, *, bet: int):
        return await slots.cmd(self, ctx, bet)

    @slots_command.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.respond(embed=EconErrors.missing_bet(ctx))
        elif isinstance(error, commands.BadArgument):
            await ctx.respond(embed=EconErrors.bad_bet_argument(ctx))
        else:
            raise error

    @commands.slash_command(
        name="stats",
        description="Display your stats (BETA)",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def stats_command(self, ctx, *, game: discord.Option(choices=["BlackJack", "Slots"])):
        return await stats.cmd(self, ctx, game)

    @stats_command.error
    async def on_command_error(self, ctx, error):
        await ctx.respond(embed=GenericErrors.default_exception(ctx))
        raise error

    @commands.command(
        name="stats",
        aliases=["stat"],
        help="Display your gambling stats, you can choose between \"blackjack\" or \"slots\"."
    )
    async def stats_command_prefix(self, ctx, *, game: str):

        if game.lower() == "blackjack" or game.lower() == "bj":
            game = "BlackJack"
        elif game.lower() == "slots" or game.lower() == "slot":
            game = "Slots"
        else:
            raise commands.BadArgument

        return await stats.cmd(self, ctx, game)

    @stats_command_prefix.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.respond(embed=EconErrors.missing_bet(ctx))
        elif isinstance(error, commands.BadArgument):
            await ctx.respond(embed=EconErrors.bad_argument(ctx))
        else:
            await ctx.respond(embed=GenericErrors.default_exception(ctx))
            raise error


def setup(client):
    client.add_cog(Economy(client))
