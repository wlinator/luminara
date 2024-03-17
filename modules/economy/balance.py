import discord
from discord.ext import commands, bridge
from dotenv import load_dotenv

from services.Currency import Currency
from lib import checks

load_dotenv('.env')


class Balance(commands.Cog):
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
    async def balance(self, ctx):
        # Currency handler
        ctx_currency = Currency(ctx.author.id)

        balance = Currency.format(ctx_currency.balance)

        embed = discord.Embed(
            color=discord.Color.embed_background(),
            description=f"**Cash**: ${balance}"
        )
        embed.set_author(name=f"{ctx.author.name}'s wallet", icon_url=ctx.author.avatar.url)

        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(Balance(client))
