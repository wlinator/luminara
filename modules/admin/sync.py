import discord
from lib.embed_builder import EmbedBuilder
from lib.exceptions.LumiExceptions import LumiException


async def sync_commands(client, ctx):
    try:
        await client.sync_commands()
        embed = EmbedBuilder.create_success_embed(
            ctx,
            author_text="Sync Successful",
            description="command tree synced successfully.",
        )
        await ctx.send(embed=embed)
    except discord.HTTPException as e:
        raise LumiException(f"An error occurred while syncing: {e}") from e
