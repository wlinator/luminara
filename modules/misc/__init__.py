import datetime
from discord.ext import commands, bridge
from lib import checks
from lib.embeds.info import MiscInfo
from lib.embeds.error import GenericErrors
from modules.misc import introduction


class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.start_time = datetime.datetime.now()

    @bridge.bridge_command(
        name="ping",
        aliases=["p", "status"],
        description="Simple status check.",
        help="Simple status check, this command will not return the latency of the bot process as this is "
             "fairly irrelevant. If the bot replies, it's good to go.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def ping(self, ctx):
        return await ctx.respond(embed=MiscInfo.ping(ctx, self.client))

    @bridge.bridge_command(
        name="uptime",
        description="Racu uptime",
        help="See how long Racu has been online, the uptime shown will reset when the Misc module is reloaded.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def uptime(self, ctx):

        unix_timestamp = int(round(self.start_time.timestamp()))
        return await ctx.respond(embed=MiscInfo.uptime(ctx, self.client, unix_timestamp))

    @bridge.bridge_command(
        name="introduction",
        aliases=["intro", "introduce"],
        guild_only=False,
        description="This command can only be done in DMs.",
        help="Introduce yourself to a server. For now this command "
             "can only be done in ONE server and only as a __slash command in Racu's DMs__."
    )
    @commands.dm_only()
    async def intro_command(self, ctx):
        return await introduction.cmd(self, ctx)

    @intro_command.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.respond(embed=GenericErrors.private_message_only(ctx))
        else:
            await ctx.respond(embed=GenericErrors.default_exception(ctx))
            raise error


def setup(client):
    client.add_cog(Misc(client))
