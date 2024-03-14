import discord
from discord.ext import commands
from dotenv import load_dotenv

from services.Currency import Currency
from lib import checks

load_dotenv('.env')


class BalanceCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        name="balance",
        description="See how much cash you have.",
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
    client.add_cog(BalanceCog(client))
