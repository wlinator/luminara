import mysql.connector
from lib.constants import CONST
from lib.embed_builder import EmbedBuilder
from lib.formatter import shorten

from db import database


async def select_cmd(ctx, query: str):
    if query.lower().startswith("select "):
        query = query[7:]

    try:
        results = database.select_query(f"SELECT {query}")
        embed = EmbedBuilder.create_success_embed(
            ctx,
            author_text=CONST.STRINGS["admin_sql_select_title"],
            description=CONST.STRINGS["admin_sql_select_description"].format(
                shorten(query, 200),
                shorten(str(results), 200),
            ),
            show_name=False,
        )
    except mysql.connector.Error as error:
        embed = EmbedBuilder.create_error_embed(
            ctx,
            author_text=CONST.STRINGS["admin_sql_select_error_title"],
            description=CONST.STRINGS["admin_sql_select_error_description"].format(
                shorten(query, 200),
                shorten(str(error), 200),
            ),
            show_name=False,
        )

    return await ctx.respond(embed=embed, ephemeral=True)


async def inject_cmd(ctx, query: str):
    try:
        database.execute_query(query)
        embed = EmbedBuilder.create_success_embed(
            ctx,
            author_text=CONST.STRINGS["admin_sql_inject_title"],
            description=CONST.STRINGS["admin_sql_inject_description"].format(
                shorten(query, 200),
            ),
            show_name=False,
        )
    except mysql.connector.Error as error:
        embed = EmbedBuilder.create_error_embed(
            ctx,
            author_text=CONST.STRINGS["admin_sql_inject_error_title"],
            description=CONST.STRINGS["admin_sql_inject_error_description"].format(
                shorten(query, 200),
                shorten(str(error), 200),
            ),
            show_name=False,
        )

    await ctx.respond(embed=embed, ephemeral=True)
