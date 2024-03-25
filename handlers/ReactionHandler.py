import random
from config.parser import JsonCache
from lib import checks


class ReactionHandler:
    def __init__(self):
        self.reactions = JsonCache.read_json("reactions")
        self.eightball = self.reactions["eightball"]
        self.full_content_reactions = self.reactions["full_content_reactions"]

    async def handle_message(self, message):
        content = message.content.lower()

        if (content.startswith("racu ") or content.startswith("racu, ")) and content.endswith("?"):
            response = random.choice(self.eightball)
            await message.reply(content=response)

        for trigger, response in self.full_content_reactions.items():
            if trigger.lower() == content:
                await message.reply(response)
