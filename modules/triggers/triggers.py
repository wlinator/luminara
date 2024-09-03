from typing import Any

import discord
from discord import app_commands
from discord.ext import commands
from reactionmenu import ViewButton, ViewMenu

import lib.format
from lib.client import Luminara
from lib.const import CONST
from lib.exceptions import LumiException
from services.reactions_service import CustomReactionsService
from ui.embeds import Builder


@app_commands.guild_only()
@app_commands.default_permissions(manage_guild=True)
class Triggers(commands.GroupCog, group_name="trigger"):
    def __init__(self, bot: Luminara):
        self.bot = bot

    add = app_commands.Group(
        name="add",
        description="Add a trigger",
        allowed_contexts=app_commands.AppCommandContext(
            guild=True,
            dm_channel=False,
            private_channel=False,
        ),
        default_permissions=discord.Permissions(manage_guild=True),
    )

    @add.command(name="response")
    async def add_text_response(
        self,
        interaction: discord.Interaction,
        trigger_text: str,
        response: str,
        is_full_match: bool = False,
    ) -> None:
        """
        Add a custom reaction that uses text.

        Parameters
        ----------
        trigger_text: str
            The text that triggers the reaction.
        response: str
            The text to respond with.
        """
        assert interaction.guild

        reaction_service = CustomReactionsService()
        guild_id: int = interaction.guild.id
        creator_id: int = interaction.user.id

        limit_reached = await reaction_service.count_custom_reactions(guild_id) >= 100
        if limit_reached:
            raise LumiException(CONST.STRINGS["trigger_limit_reached"])

        existing_trigger = await reaction_service.find_trigger(guild_id, trigger_text)
        if existing_trigger:
            raise LumiException(CONST.STRINGS["trigger_already_exists"])

        success: bool = await reaction_service.create_custom_reaction(
            guild_id=guild_id,
            creator_id=creator_id,
            trigger_text=trigger_text,
            response=response,
            emoji_id=None,
            is_emoji=False,
            is_full_match=is_full_match,
            is_global=False,
        )

        if not success:
            raise LumiException(CONST.STRINGS["triggers_not_added"])

        embed = Builder.create_embed(
            Builder.SUCCESS,
            user_name=interaction.user.name,
            author_text=CONST.STRINGS["triggers_add_author"],
            description="",
            footer_text=CONST.STRINGS["triggers_reaction_service_footer"],
            hide_name_in_description=True,
        )

        embed.description += CONST.STRINGS["triggers_add_description"].format(
            lib.format.shorten(trigger_text, 50),
            CONST.STRINGS["triggers_type_text"],
            is_full_match,
        )
        embed.description += CONST.STRINGS["triggers_add_text_details"].format(lib.format.shorten(response, 50))

        await interaction.response.send_message(embed=embed)

    @add.command(name="emoji")
    async def add_emoji_response(
        self,
        interaction: discord.Interaction,
        trigger_text: str,
        emoji_id: int,
        is_full_match: bool = False,
    ) -> None:
        """
        Add a custom reaction that uses an emoji.

        Parameters
        ----------
        trigger_text: str
            The text that triggers the reaction.
        emoji_id: int
            The ID of the emoji to use.
        """
        assert interaction.guild

        reaction_service = CustomReactionsService()
        guild_id: int = interaction.guild.id
        creator_id: int = interaction.user.id

        limit_reached = await reaction_service.count_custom_reactions(guild_id) >= 100
        if limit_reached:
            raise LumiException(CONST.STRINGS["trigger_limit_reached"])

        existing_trigger = await reaction_service.find_trigger(guild_id, trigger_text)
        if existing_trigger:
            raise LumiException(CONST.STRINGS["trigger_already_exists"])

        success: bool = await reaction_service.create_custom_reaction(
            guild_id=guild_id,
            creator_id=creator_id,
            trigger_text=trigger_text,
            response=None,
            emoji_id=emoji_id,
            is_emoji=True,
            is_full_match=is_full_match,
            is_global=False,
        )

        if not success:
            raise LumiException(CONST.STRINGS["triggers_not_added"])

        embed = Builder.create_embed(
            Builder.SUCCESS,
            user_name=interaction.user.name,
            author_text=CONST.STRINGS["triggers_add_author"],
            description="",
            footer_text=CONST.STRINGS["triggers_reaction_service_footer"],
            hide_name_in_description=True,
        )

        embed.description += CONST.STRINGS["triggers_add_description"].format(
            lib.format.shorten(trigger_text, 50),
            CONST.STRINGS["triggers_type_emoji"],
            is_full_match,
        )
        embed.description += CONST.STRINGS["triggers_add_emoji_details"].format(emoji_id)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="delete")
    async def remove_text_response(
        self,
        interaction: discord.Interaction,
        reaction_id: int,
    ) -> None:
        """
        Delete a custom reaction by its ID.

        Parameters
        ----------
        reaction_id: int
            The ID of the reaction to delete.
        """
        assert interaction.guild

        reaction_service = CustomReactionsService()
        guild_id: int = interaction.guild.id
        reaction = await reaction_service.find_id(reaction_id)

        if reaction is None or reaction["guild_id"] != guild_id or reaction["is_global"]:
            raise LumiException(CONST.STRINGS["triggers_not_found"])

        await reaction_service.delete_custom_reaction(reaction_id)

        embed = Builder.create_embed(
            Builder.SUCCESS,
            user_name=interaction.user.name,
            author_text=CONST.STRINGS["triggers_delete_author"],
            description=CONST.STRINGS["triggers_delete_description"],
            footer_text=CONST.STRINGS["triggers_reaction_service_footer"],
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="list")
    async def list_reactions(self, interaction: discord.Interaction) -> None:
        """
        List all custom reactions for the current guild.

        Parameters
        ----------
        interaction: discord.Interaction
            The interaction to list the reactions for.
        """
        assert interaction.guild
        reaction_service: CustomReactionsService = CustomReactionsService()
        guild_id: int = interaction.guild.id

        reactions: list[dict[str, Any]] = await reaction_service.find_all_by_guild(guild_id)
        if not reactions:
            embed: discord.Embed = Builder.create_embed(
                Builder.WARNING,
                user_name=interaction.user.name,
                author_text=CONST.STRINGS["triggers_no_reactions_title"],
                description=CONST.STRINGS["triggers_no_reactions_description"],
                footer_text=CONST.STRINGS["triggers_reaction_service_footer"],
                hide_name_in_description=True,
            )
            await interaction.response.send_message(embed=embed)
            return

        menu = ViewMenu(interaction, menu_type=ViewMenu.TypeEmbed, all_can_click=True, remove_items_on_timeout=True)

        for reaction in reactions:
            embed: discord.Embed = Builder.create_embed(
                Builder.SUCCESS,
                user_name=interaction.user.name,
                title=CONST.STRINGS["triggers_list_custom_reaction_id"].format(
                    reaction["id"],
                ),
                author_text=CONST.STRINGS["triggers_list_custom_reactions_title"],
                footer_text=CONST.STRINGS["triggers_reaction_service_footer"],
                hide_name_in_description=True,
            )

            description_lines = [
                CONST.STRINGS["triggers_list_trigger_text"].format(
                    lib.format.shorten(reaction["trigger_text"], 50),
                ),
                CONST.STRINGS["triggers_list_reaction_type"].format(
                    CONST.STRINGS["triggers_type_emoji"]
                    if reaction["is_emoji"]
                    else CONST.STRINGS["triggers_type_text"],
                ),
            ]

            if reaction["is_emoji"]:
                description_lines.append(
                    CONST.STRINGS["triggers_list_emoji_id"].format(reaction["emoji_id"]),
                )
            else:
                description_lines.append(
                    CONST.STRINGS["triggers_list_response"].format(
                        lib.format.shorten(reaction["response"], 50),
                    ),
                )

            description_lines.extend(
                [
                    CONST.STRINGS["triggers_list_full_match"].format(
                        "True" if reaction["is_full_match"] else "False",
                    ),
                    CONST.STRINGS["triggers_list_usage_count"].format(
                        reaction["usage_count"],
                    ),
                ],
            )

            embed.description = "\n".join(description_lines)
            menu.add_page(embed)

        buttons = [
            (ViewButton.ID_GO_TO_FIRST_PAGE, "⏮️"),
            (ViewButton.ID_PREVIOUS_PAGE, "⏪"),
            (ViewButton.ID_NEXT_PAGE, "⏩"),
            (ViewButton.ID_GO_TO_LAST_PAGE, "⏭️"),
        ]

        for custom_id, emoji in buttons:
            menu.add_button(ViewButton(style=discord.ButtonStyle.secondary, custom_id=custom_id, emoji=emoji))

        await menu.start()


async def setup(bot: Luminara) -> None:
    await bot.add_cog(Triggers(bot))
