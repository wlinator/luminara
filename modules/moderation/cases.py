import asyncio

import discord
from discord.ext import commands
from reactionmenu import ViewButton, ViewMenu

from lib.case_handler import edit_case_modlog
from lib.const import CONST
from lib.exceptions import LumiException
from lib.format import format_case_number
from services.case_service import CaseService
from ui.cases import (
    create_case_embed,
    create_case_list_embed,
)
from ui.embeds import Builder

case_service = CaseService()


def create_no_cases_embed(ctx: commands.Context[commands.Bot], author_text: str, description: str) -> discord.Embed:
    return Builder.create_embed(
        theme="info",
        user_name=ctx.author.name,
        author_text=author_text,
        description=description,
    )


def create_case_view_menu(ctx: commands.Context[commands.Bot]) -> ViewMenu:
    menu = ViewMenu(ctx, menu_type=ViewMenu.TypeEmbed, all_can_click=True, delete_on_timeout=True)

    buttons = [
        (ViewButton.ID_GO_TO_FIRST_PAGE, "⏮️"),
        (ViewButton.ID_PREVIOUS_PAGE, "⏪"),
        (ViewButton.ID_NEXT_PAGE, "⏩"),
        (ViewButton.ID_GO_TO_LAST_PAGE, "⏭️"),
    ]

    for custom_id, emoji in buttons:
        menu.add_button(ViewButton(style=discord.ButtonStyle.secondary, custom_id=custom_id, emoji=emoji))

    return menu


class Cases(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="case", aliases=["c", "ca"])
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def view_case_by_number(
        self,
        ctx: commands.Context[commands.Bot],
        case_number: int | None = None,
    ) -> None:
        """
        View a specific case by number or all cases if no number is provided.

        Parameters
        ----------
        case_number: int | None
            The case number to view. If None, view all cases.
        """
        if case_number is None:
            await ctx.invoke(self.view_all_cases_in_guild)
            return

        guild_id = ctx.guild.id if ctx.guild else 0
        case = case_service.fetch_case_by_guild_and_number(guild_id, case_number)

        if not case:
            embed = create_no_cases_embed(
                ctx,
                CONST.STRINGS["error_no_case_found_author"],
                CONST.STRINGS["error_no_case_found_description"],
            )
            await ctx.send(embed=embed)
            return

        target = await commands.UserConverter().convert(ctx, str(case["target_id"]))
        embed: discord.Embed = create_case_embed(
            ctx=ctx,
            target=target,
            case_number=case["case_number"],
            action_type=case["action_type"],
            reason=case["reason"],
            timestamp=case["created_at"],
            duration=case["duration"] or None,
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="cases")
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def view_all_cases_in_guild(
        self,
        ctx: commands.Context[commands.Bot],
    ) -> None:
        """
        View all cases in the guild.

        Parameters
        ----------
        ctx: commands.Context[commands.Bot]
            The context of the command.
        """
        if not ctx.guild:
            raise LumiException(CONST.STRINGS["error_not_in_guild"])

        guild_id = ctx.guild.id
        cases = case_service.fetch_cases_by_guild(guild_id)

        if not cases:
            embed = create_no_cases_embed(
                ctx,
                CONST.STRINGS["case_guild_no_cases_author"],
                CONST.STRINGS["case_guild_no_cases"],
            )
            await ctx.send(embed=embed)
            return

        menu = create_case_view_menu(ctx)

        for i in range(0, len(cases), 10):
            chunk = cases[i : i + 10]
            embed = create_case_list_embed(
                ctx,
                chunk,
                CONST.STRINGS["case_guild_cases_author"],
            )
            menu.add_page(embed)

        await menu.start()

    @commands.hybrid_command(name="modcases", aliases=["mc", "modc"])
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def view_all_cases_by_mod(
        self,
        ctx: commands.Context[commands.Bot],
        moderator: discord.Member,
    ) -> None:
        """
        View all cases by a specific moderator.

        Parameters
        ----------
        moderator: discord.Member
            The moderator to view cases for.
        """
        if not ctx.guild:
            raise LumiException(CONST.STRINGS["error_not_in_guild"])

        guild_id = ctx.guild.id
        cases = case_service.fetch_cases_by_moderator(guild_id, moderator.id)

        if not cases:
            embed = create_no_cases_embed(
                ctx,
                CONST.STRINGS["case_mod_no_cases_author"],
                CONST.STRINGS["case_mod_no_cases"],
            )
            await ctx.send(embed=embed)
            return

        menu = create_case_view_menu(ctx)

        for i in range(0, len(cases), 10):
            chunk = cases[i : i + 10]
            embed = create_case_list_embed(
                ctx,
                chunk,
                CONST.STRINGS["case_mod_cases_author"].format(moderator.name),
            )
            menu.add_page(embed)

        await menu.start()

    @commands.hybrid_command(name="editcase", aliases=["ec", "uc"])
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def edit_case_reason(
        self,
        ctx: commands.Context[commands.Bot],
        case_number: int,
        *,
        new_reason: str,
    ) -> None:
        """
        Edit the reason for a specific case.

        Parameters
        ----------
        case_number: int
            The case number to edit.
        new_reason: str
            The new reason for the case.
        """
        if not ctx.guild:
            raise LumiException(CONST.STRINGS["error_not_in_guild"])

        guild_id = ctx.guild.id

        case_service.edit_case_reason(
            guild_id,
            case_number,
            new_reason,
        )

        embed = Builder.create_embed(
            theme="success",
            user_name=ctx.author.name,
            author_text=CONST.STRINGS["case_reason_update_author"],
            description=CONST.STRINGS["case_reason_update_description"].format(
                format_case_number(case_number),
            ),
        )

        async def update_tasks():
            await asyncio.gather(
                ctx.send(embed=embed),
                edit_case_modlog(ctx, guild_id, case_number, new_reason),
            )

        await update_tasks()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Cases(bot))
