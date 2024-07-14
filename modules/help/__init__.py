from discord.ext import commands

from lib import formatter, embed_builder, constants


class Help(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.slash_command(
        name="help",
        description="Get Lumi help.",
    )
    async def help_command(self, ctx) -> None:
        prefix = formatter.get_prefix(ctx)
        embed = embed_builder.EmbedBuilder.create_warning_embed(
            ctx=ctx,
            description=constants.CONST.STRINGS["help_use_prefix"].format(prefix),
        )
        await ctx.respond(embed=embed, ephemeral=True)


def setup(client: commands.Bot) -> None:
    client.add_cog(Help(client))
