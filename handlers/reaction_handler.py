from discord import Message
from discord.ext.commands import Cog
from loguru import logger

from services.reactions_service import CustomReactionsService
from services.blacklist_service import BlacklistUserService


class ReactionHandler:
    """
    Handles reactions to messages based on predefined triggers and responses.
    """

    def __init__(self, client, message: Message) -> None:
        self.client = client
        self.message: Message = message
        self.content: str = self.message.content.lower()
        self.reaction_service = CustomReactionsService()

    async def run_checks(self) -> None:
        """
        Runs checks for reactions and responses.
        Guild triggers are prioritized over global triggers if they are identical.
        """
        guild_id = self.message.guild.id if self.message.guild else None

        if guild_id:
            data = await self.reaction_service.find_trigger(guild_id, self.content)
            if data:
                processed = False
                try:
                    if data["type"] == "text":
                        processed = await self.try_respond(data)
                    elif data["type"] == "emoji":
                        processed = await self.try_react(data)
                except Exception as e:
                    logger.warning(f"Failed to process reaction: {e}")

                if processed:
                    await self.reaction_service.increment_reaction_usage(
                        int(data["id"]),
                    )

    async def try_respond(self, data) -> bool:
        """
        Tries to respond to the message.
        """
        response = data.get("response")
        if response:
            try:
                await self.message.reply(response)
                return True
            except Exception:
                pass
        return False

    async def try_react(self, data) -> bool:
        """
        Tries to react to the message.
        """
        emoji_id = data.get("emoji_id")
        if emoji_id:
            try:
                emoji = self.client.get_emoji(emoji_id)
                if emoji:
                    await self.message.add_reaction(emoji)
                    return True
            except Exception:
                pass
        return False


class ReactionListener(Cog):
    def __init__(self, client) -> None:
        self.client = client

    @Cog.listener("on_message")
    async def reaction_listener(self, message: Message) -> None:
        """
        Listens for new messages and processes them if the author is not a bot and not blacklisted.

        :param message: The message to process.
        """
        if not message.author.bot and not BlacklistUserService.is_user_blacklisted(
            message.author.id,
        ):
            await ReactionHandler(self.client, message).run_checks()


def setup(client) -> None:
    client.add_cog(ReactionListener(client))
