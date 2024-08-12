import discord
from discord.ext.commands import guild_only
from discord.ext import bridge, commands

from modules.levels import leaderboard, level


class Levels(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @bridge.bridge_command(
        name="level",
        aliases=["rank", "xp"],
        description="Displays your level and server rank.",
        help="Displays your level and server rank.",
        contexts={discord.InteractionContextType.guild},
    )
    @guild_only()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def level_command(self, ctx) -> None:
        await level.rank(ctx)

    @bridge.bridge_command(
        name="leaderboard",
        aliases=["lb", "xplb"],
        description="See the Lumi leaderboards.",
        help="Shows three different leaderboards: levels, currency and daily streaks.",
        contexts={discord.InteractionContextType.guild},
    )
    @guild_only()
    @commands.cooldown(1, 180, commands.BucketType.user)
    async def leaderboard_command(self, ctx) -> None:
        await leaderboard.cmd(ctx)


def setup(client: commands.Bot) -> None:
    client.add_cog(Levels(client))
