from discord import TextChannel
from discord.ext import commands

from lib.client import Luminara
from lib.const import CONST
from lib.exceptions import LumiException
from services.feed_service import FeedService
from ui.embeds import Builder
from wrappers.twitch import TwitchClient


class TwitchFeed(commands.Cog):
    def __init__(self, bot: Luminara) -> None:
        self.bot = bot
        self.feed_service = FeedService()
        self.twitch_client = TwitchClient()

    @commands.group(
        name="feed",
        description="Manage feeds.",
        guild_only=True,
    )
    async def feed_group(self, ctx: commands.Context[Luminara]) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send("Please specify a subcommand for feed, such as `twitch`.")

    @feed_group.command(
        name="twitch",
        description="Add a new Twitch feed to the server.",
    )
    @commands.has_permissions(manage_guild=True)
    async def add_feed(
        self,
        ctx: commands.Context[Luminara],
        twitch_username: str,
        channel: TextChannel,
        *,
        announcement_message: str,
    ) -> None:
        """
        Adds a new Twitch feed with the specified username, channel, and announcement message.

        Parameters
        ----------
        ctx : commands.Context
            The context of the command.
        twitch_username : str
            The Twitch username to track.
        channel : discord.TextChannel
            The Discord channel where announcements will be posted.
        announcement_message : str
            The message to announce when the Twitch user streams.
        """
        assert ctx.guild

        try:
            if not self.twitch_client.check_account_exists(twitch_username):
                msg = f"Twitch username '{twitch_username}' does not exist."
                await ctx.send(embed=Builder.create_embed(Builder.ERROR, user_name=ctx.author.name, description=msg))
                return

            # Upsert the new feed into the database
            self.feed_service.upsert_feed(
                guild_id=ctx.guild.id,
                channel_id=channel.id,
                announcement_message=announcement_message,
                feed_type="twitch",
                username=twitch_username,
            )

            # Create a success embed
            embed = Builder.create_embed(
                Builder.SUCCESS,
                user_name=ctx.author.name,
                description=CONST.STRINGS["add_feed_success"].format(twitch_username, channel.mention),
            )
            await ctx.send(embed=embed)

        except LumiException as le:
            # Handle custom Lumi exceptions
            embed = Builder.create_embed(
                Builder.ERROR,
                user_name=ctx.author.name,
                description=str(le),
            )
            await ctx.send(embed=embed)

        except Exception as e:
            # Handle unexpected exceptions
            embed = Builder.create_embed(
                Builder.ERROR,
                user_name=ctx.author.name,
                description=CONST.STRINGS["add_feed_failure"].format(str(e)),
            )
            await ctx.send(embed=embed)


async def setup(bot: Luminara) -> None:
    await bot.add_cog(TwitchFeed(bot))
