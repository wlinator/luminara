import random

from discord.ext.commands import Cog

from config.parser import JsonCache

_reactions = JsonCache.read_json("reactions")
_8ball = _reactions["eightball"]
_full = _reactions["full_content_reactions"]


class ReactionHandler:

    @staticmethod
    async def respond(message):
        content = message.content.lower()

        if (content.startswith("racu ") or content.startswith("racu, ")) and content.endswith("?"):
            response = random.choice(_8ball)
            await message.reply(content=response)

        for trigger, response in _full.items():
            if trigger.lower() == content:
                await message.reply(response)


class ReactionListener(Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener('on_message')
    async def reaction_listener(self, message):
        if not message.author.bot:
            await ReactionHandler.respond(message)


def setup(client):
    client.add_cog(ReactionListener(client))
