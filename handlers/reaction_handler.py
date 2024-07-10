import random
import asyncio
from typing import List, Dict, Any

import discord
from discord.ext.commands import Cog, Context, EmojiConverter
from discord import Message

from config.parser import JsonCache
from services.blacklist_service import BlacklistUserService


class ReactionHandler:
    """
    Handles reactions to messages based on predefined triggers and responses.
    """
    
    def __init__(self, client, message: Message) -> None:
        self.reactions: Dict[str, Any] = JsonCache.read_json("reactions")
        self.eightball: List[str] = self.reactions["eightball"]
        self.full_response: Dict[str, str] = self.reactions["full_content_responses"]
        self.partial_react: Dict[str, str] = self.reactions["partial_content_reactions"]
        self.message: Message = message
        self.content: str = self.message.content.lower()
        self.client = client
    
    async def run_all_checks(self) -> None:
        """
        Runs all checks for reactions and responses.
        """
        await asyncio.gather(
            self.check_eightball(self.eightball),
            self.check_full_response(),
            self.react()
        )
    
    async def check_eightball(self, choices: List[str]) -> None:
        """
        Checks if the message is a question directed at Lumi and responds with a random choice.
        
        :param choices: List of possible responses.
        """
        if (self.content.startswith("lumi ") or self.content.startswith("lumi, ")) and self.content.endswith("?"):
            response: str = random.choice(choices)
            await self.message.reply(content=response)
    
    async def check_full_response(self) -> None:
        """
        Checks if the message content matches any full content triggers and responds accordingly.
        """
        for trigger, response in self.full_response.items():
            if trigger.lower() == self.content:
                await self.message.reply(response)

    async def react(self) -> None:
        """
        Adds reactions to the message based on partial content triggers.
        """
        ctx = await self.client.get_context(self.message)
        for trigger, emoji in self.partial_react.items():
            if trigger.lower() in self.content:
                emoji = await self.client.convert_to_emoji(ctx, emoji)
                if emoji:
                    await self.message.add_reaction(emoji)


class ReactionListener(Cog):
    def __init__(self, client) -> None:
        self.client = client

    @Cog.listener('on_message')
    async def reaction_listener(self, message: Message) -> None:
        """
        Listens for new messages and processes them if the author is not a bot and not blacklisted.
        
        :param message: The message to process.
        """
        if not message.author.bot and not BlacklistUserService.is_user_blacklisted(message.author.id):
            await ReactionHandler(self.client, message).run_all_checks()


def setup(client) -> None:
    client.add_cog(ReactionListener(client))
