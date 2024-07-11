from discord.commands import SlashCommandGroup
from discord.ext import commands
import discord

from Client import LumiBot
from modules.triggers.add import add_reaction


class Triggers(commands.Cog):
    def __init__(self, client: LumiBot):
        self.client = client

    trigger = SlashCommandGroup(
        "trigger", "Manage custom reactions.", guild_only=True, default_member_permissions=discord.Permissions(manage_guild=True)
    )
    add = trigger.create_subgroup("add", "Add new custom reactions.")

    @add.command(
        name="response",
        description="Add a new custom text reaction.",
        help="Add a new custom text reaction to the database.",
    )
    @commands.guild_only()
    async def add_text_reaction_command(
        self,
        ctx,
        trigger_text: str,
        response: str,
        is_full_match: bool
    ):
        await add_reaction(ctx, trigger_text, response, None, False, is_full_match)

    @add.command(
        name="emoji",
        description="Add a new custom emoji reaction.",
        help="Add a new custom emoji reaction to the database.",
    )
    @commands.guild_only()
    async def add_emoji_reaction_command(
        self,
        ctx,
        trigger_text: str,
        emoji: discord.Emoji,
        is_full_match: bool
    ):
        await add_reaction(ctx, trigger_text, None, emoji.id, True, is_full_match)

def setup(client: LumiBot):
    client.add_cog(Triggers(client))