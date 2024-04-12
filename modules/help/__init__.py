from discord.ext import commands

import lib.formatter
import lib.checks


class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        name="help",
        description="Get Racu help.",
    )
    @lib.checks.allowed_in_channel()
    async def help_command(self, ctx):
        prefix = lib.formatter.get_prefix(ctx)
        return await ctx.respond(content=f"Please use Racu's prefix to get help. Type `{prefix}help`", ephemeral=True)


def setup(client):
    client.add_cog(Help(client))
