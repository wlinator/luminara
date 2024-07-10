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

    async def run_all_checks(self) -> None:
        """
        Runs all checks for reactions and responses.
        """
        guild_id = self.message.guild.id if self.message.guild else None

        if guild_id:
            reaction = await self.reaction_service.find_trigger(guild_id, self.content)
            if reaction:
                processed = False
                try:
                    if reaction["type"] == "text":
                        await self.message.reply(reaction["response"])
                        processed = True
                    elif reaction["type"] == "emoji":
                        await self.message.add_reaction(reaction["response"])
                        processed = True
                except Exception as e:
                    logger.warning(f"Failed to process reaction: {e}")

                if processed:
                    await self.reaction_service.increment_reaction_usage(
                        int(reaction["id"])
                    )


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
            message.author.id
        ):
            await ReactionHandler(self.client, message).run_all_checks()


def setup(client) -> None:
    client.add_cog(ReactionListener(client))
