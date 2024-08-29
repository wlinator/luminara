import discord
from discord.ext import commands

from lib.const import CONST
from services.currency_service import Currency
from ui.embeds import Builder


class Award(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="award")
    @commands.is_owner()
    async def award_command(self, ctx: commands.Context[commands.Bot], user: discord.User, amount: int) -> None:
        curr = Currency(user.id)
        curr.add_balance(amount)
        curr.push()

        embed = Builder.create_embed(
            theme="success",
            user_name=ctx.author.name,
            author_text=CONST.STRINGS["admin_award_title"],
            description=CONST.STRINGS["admin_award_description"].format(
                Currency.format(amount),
                user.name,
            ),
        )

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Award(bot))
