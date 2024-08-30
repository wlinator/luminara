import contextlib
from typing import Any

from discord import Message
from discord.ext import commands
from loguru import logger

from lib.client import Luminara
from services.blacklist_service import BlacklistUserService
from services.reactions_service import CustomReactionsService


class ReactionHandler:
    """
    Handles reactions to messages based on predefined triggers and responses.
    """

    def __init__(self, bot: Luminara, message: Message) -> None:
        self.bot = bot
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

    async def try_respond(self, data: dict[str, Any]) -> bool:
        """
        Tries to respond to the message.
        """
        if response := data.get("response"):
            with contextlib.suppress(Exception):
                await self.message.reply(response)
                return True
        return False

    async def try_react(self, data: dict[str, Any]) -> bool:
        """
        Tries to react to the message.
        """
        if emoji_id := data.get("emoji_id"):
            with contextlib.suppress(Exception):
                if emoji := self.bot.get_emoji(emoji_id):
                    await self.message.add_reaction(emoji)
                    return True
        return False


class ReactionListener(commands.Cog):
    def __init__(self, bot: Luminara) -> None:
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def reaction_listener(self, message: Message) -> None:
        """
        Listens for new messages and processes them if the author is not a bot and not blacklisted.

        :param message: The message to process.
        """
        if not message.author.bot and not BlacklistUserService.is_user_blacklisted(
            message.author.id,
        ):
            await ReactionHandler(self.bot, message).run_checks()


async def setup(bot: Luminara) -> None:
    await bot.add_cog(ReactionListener(bot))
