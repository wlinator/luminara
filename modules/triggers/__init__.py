from discord.commands import SlashCommandGroup
from discord.ext import commands
import discord

from Client import LumiBot
from modules.triggers.add import add_reaction
from modules.triggers.delete import delete_reaction
from modules.triggers.list import list_reactions


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
    
    @trigger.command(
        name="delete",
        description="Delete an existing custom reaction.",
        help="Delete an existing custom reaction from the database.",
    )
    @commands.guild_only()
    async def delete_reaction_command(
        self,
        ctx,
        reaction_id: int
    ):
        await delete_reaction(ctx, reaction_id)
    
    @trigger.command(
        name="list",
        description="List all custom reactions.",
        help="List all custom reactions for the current guild.",
    )
    @commands.guild_only()
    async def list_reactions_command(
        self,
        ctx
    ):
        await list_reactions(ctx)

def setup(client: LumiBot):
    client.add_cog(Triggers(client))