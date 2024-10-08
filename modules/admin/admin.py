import mysql.connector
from discord.ext import commands

import lib.format
from db import database
from lib.client import Luminara
from lib.const import CONST
from lib.format import shorten
from ui.embeds import Builder


class Sql(commands.Cog):
    def __init__(self, bot: Luminara):
        self.bot = bot
        self.select_cmd.usage = lib.format.generate_usage(self.select_cmd)
        self.inject_cmd.usage = lib.format.generate_usage(self.inject_cmd)

    @commands.command(name="sqlselect", aliases=["sqls"])
    @commands.is_owner()
    async def select_cmd(
        self,
        ctx: commands.Context[Luminara],
        *,
        query: str,
    ) -> None:
        """
        Execute a SQL SELECT query.

        Parameters
        ----------
        ctx : commands.Context[Luminara]
            The context of the command.
        query : str
            The SQL query to execute.
        """
        if query.lower().startswith("select "):
            query = query[7:]

        try:
            results = database.select_query(f"SELECT {query}")
            embed = Builder.create_embed(
                Builder.SUCCESS,
                user_name=ctx.author.name,
                author_text=CONST.STRINGS["admin_sql_select_title"],
                description=CONST.STRINGS["admin_sql_select_description"].format(
                    shorten(query, 200),
                    shorten(str(results), 200),
                ),
                hide_name_in_description=True,
            )
        except mysql.connector.Error as error:
            embed = Builder.create_embed(
                Builder.ERROR,
                user_name=ctx.author.name,
                author_text=CONST.STRINGS["admin_sql_select_error_title"],
                description=CONST.STRINGS["admin_sql_select_error_description"].format(
                    shorten(query, 200),
                    shorten(str(error), 200),
                ),
                hide_name_in_description=True,
            )

        await ctx.send(embed=embed, ephemeral=True)

    @commands.command(name="sqlinject", aliases=["sqli"])
    @commands.is_owner()
    async def inject_cmd(
        self,
        ctx: commands.Context[Luminara],
        *,
        query: str,
    ) -> None:
        """
        Execute a SQL INJECT query.

        Parameters
        ----------
        ctx : commands.Context[Luminara]
            The context of the command.
        query : str
            The SQL query to execute.
        """
        try:
            database.execute_query(query)
            embed = Builder.create_embed(
                Builder.SUCCESS,
                user_name=ctx.author.name,
                author_text=CONST.STRINGS["admin_sql_inject_title"],
                description=CONST.STRINGS["admin_sql_inject_description"].format(
                    shorten(query, 200),
                ),
                hide_name_in_description=True,
            )
        except mysql.connector.Error as error:
            embed = Builder.create_embed(
                Builder.ERROR,
                user_name=ctx.author.name,
                author_text=CONST.STRINGS["admin_sql_inject_error_title"],
                description=CONST.STRINGS["admin_sql_inject_error_description"].format(
                    shorten(query, 200),
                    shorten(str(error), 200),
                ),
                hide_name_in_description=True,
            )

        await ctx.send(embed=embed, ephemeral=True)


async def setup(bot: Luminara) -> None:
    await bot.add_cog(Sql(bot))
