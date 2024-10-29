from discord.ext import commands

from lib.client import Luminara
from wrappers.openai import OpenAIWrapper


class OpenAI(commands.Cog):
    def __init__(self, bot: Luminara):
        self.bot = bot
        self.openai_wrapper = OpenAIWrapper()

    @commands.command(name="openai", aliases=["ai", "gpt"], help="Send a query to OpenAI and get a response.")
    @commands.is_owner()
    async def openai_command(self, ctx: commands.Context[Luminara], *, query: str) -> None:
        """
        Send a query to OpenAI and display the response.

        Parameters
        ----------
        ctx : commands.Context[Luminara]
            The context of the command.
        query : str
            The user's query to OpenAI.
        """
        response = await self.openai_wrapper.get_response(query)
        await ctx.send(response)


async def setup(bot: Luminara) -> None:
    await bot.add_cog(OpenAI(bot))
