from datetime import datetime

import discord
from discord.commands import SlashCommandGroup
from discord.ext import bridge, commands, tasks

from Client import LumiBot
from lib import checks
from modules.config import set_prefix
from modules.misc import avatar, backup, info, introduction, invite, ping, xkcd


class Misc(commands.Cog):
    def __init__(self, client: LumiBot) -> None:
        self.client: LumiBot = client
        self.start_time: datetime = datetime.now()
        self.do_backup.start()

    @tasks.loop(hours=1)
    async def do_backup(self) -> None:
        await backup.backup()

    @bridge.bridge_command(
        name="avatar",
        aliases=["av"],
        description="Get a user's avatar.",
        help="Get a user's avatar.",
        guild_only=True,
    )
    @commands.guild_only()
    @checks.allowed_in_channel()
    async def avatar(self, ctx, user: discord.Member) -> None:
        return await avatar.get_avatar(ctx, user)

    @bridge.bridge_command(
        name="ping",
        aliases=["p", "status"],
        description="Simple status check.",
        help="Simple status check.",
    )
    @checks.allowed_in_channel()
    async def ping(self, ctx) -> None:
        await ping.ping(self, ctx)

    @bridge.bridge_command(
        name="uptime",
        description="See Lumi's uptime since the last update.",
        help="See how long Lumi has been online since his last update.",
    )
    @checks.allowed_in_channel()
    async def uptime(self, ctx) -> None:
        await ping.uptime(self, ctx, self.start_time)

    @bridge.bridge_command(
        name="invite",
        description="Generate an invite link.",
        help="Generate a link to invite Lumi to your own server!",
    )
    @checks.allowed_in_channel()
    async def invite_command(self, ctx) -> None:
        await invite.cmd(ctx)

    @bridge.bridge_command(
        name="prefix",
        description="See the server's current prefix.",
        help="See the server's current prefix.",
        guild_only=True,
    )
    @commands.guild_only()
    @checks.allowed_in_channel()
    async def prefix_command(self, ctx) -> None:
        await set_prefix.get_cmd(ctx)

    @bridge.bridge_command(
        name="info",
        aliases=["stats"],
        description="Shows basic Lumi stats.",
        help="Shows basic Lumi stats.",
    )
    @checks.allowed_in_channel()
    async def info_command(self, ctx) -> None:
        unix_timestamp: int = int(round(self.start_time.timestamp()))
        await info.cmd(self, ctx, unix_timestamp)

    @bridge.bridge_command(
        name="introduction",
        aliases=["intro", "introduce"],
        guild_only=False,
        description="This command can only be used in DMs.",
        help="Introduce yourself. For now this command "
        "can only be done in ONE server and only in Lumi's DMs.",
    )
    @commands.dm_only()
    async def intro_command(self, ctx) -> None:
        await introduction.cmd(self, ctx)

    """
    xkcd submodule - slash command only
    """
    xkcd: SlashCommandGroup = SlashCommandGroup(
        "xkcd",
        "A web comic of romance, sarcasm, math, and language.",
        guild_only=False,
    )

    @xkcd.command(name="latest", description="Get the latest xkcd comic.")
    async def xkcd_latest(self, ctx) -> None:
        await xkcd.print_comic(ctx, latest=True)

    @xkcd.command(name="random", description="Get a random xkcd comic.")
    async def xkcd_random(self, ctx) -> None:
        await xkcd.print_comic(ctx)

    @xkcd.command(name="search", description="Search for a xkcd comic by ID.")
    async def xkcd_search(self, ctx, *, id: int) -> None:
        await xkcd.print_comic(ctx, number=id)


def setup(client: LumiBot) -> None:
    client.add_cog(Misc(client))
