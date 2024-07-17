import sqlite3

from db import database


async def select_cmd(ctx, query: str):
    if query.lower().startswith("select "):
        query = query[7:]

    try:
        results = database.select_query(f"SELECT {query}")
    except sqlite3.Error as error:
        results = error

    return await ctx.respond(
        content=f"```SELECT {query}```\n```{results}```",
        ephemeral=True,
    )


async def inject_cmd(ctx, query: str):
    try:
        database.execute_query(query)
        await ctx.respond(content=f"That worked!\n```{query}```", ephemeral=True)
    except sqlite3.Error as error:
        await ctx.respond(
            content=f"Query:\n```{query}```\nError message:\n```{error}```",
            ephemeral=True,
        )
