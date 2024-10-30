from discord.ext import commands

from lib.client import Luminara
from wrappers.openai import OpenAIWrapper


class OpenAI(commands.Cog):
    def __init__(self, bot: Luminara):
        self.bot = bot
        self.openai_wrapper = OpenAIWrapper()

    @commands.command(
        name="openai",
        aliases=["ai", "gpt"],
        help="Send a query to an OpenAI compatible model and get a response.",
    )
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
        # Handle attachments
        attachment = ctx.message.attachments[0] if ctx.message.attachments else None
        image_url = None
        image_info = ""

        if attachment:
            image_url = attachment.url
            image_info = f"\nImage URL: {image_url}"

        response = await self.openai_wrapper.get_response(query + image_info)

        await ctx.send(response)


async def setup(bot: Luminara) -> None:
    await bot.add_cog(OpenAI(bot))
