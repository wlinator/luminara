import discord

trigger_list=[
    "good bot",
    "racu"
]


async def check_for_reaction(message):
    content = message.content.lower()

    # check if whole message = trigger
    if content in trigger_list:
        if content == trigger_list[0]:
            await message.reply(content="Thanks!")

    # check if trigger is in message
    if trigger_list[1] in content:
        await message.add_reaction("❤️")