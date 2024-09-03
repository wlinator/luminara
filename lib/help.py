import os
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import discord
from discord.ext import commands

from lib.const import CONST
from ui.embeds import Builder


class LuminaraHelp(commands.HelpCommand):
    def __init__(self):
        """Initializes the LuminaraHelp command with necessary attributes."""
        super().__init__(
            command_attrs={
                "help": "Lists all commands and sub-commands.",
                "aliases": ["h"],
                "usage": "$help <command> or <sub-command>",
            },
        )

    async def _get_prefix(self) -> str:
        """
        Dynamically fetches the prefix from the context or uses a default prefix constant.

        Returns
        -------
        str
            The prefix used to invoke the bot.
        """
        return "."

    def _embed_base(self, author: str, description: str | None = None) -> discord.Embed:
        """
        Creates a base embed with uniform styling.

        Parameters
        ----------
        title : str
            The title of the embed.
        description : str | None
            The description of the embed.

        Returns
        -------
        discord.Embed
            The created embed.
        """
        return Builder.create_embed(
            Builder.INFO,
            author_text=author,
            description=description,
            footer_text=CONST.STRINGS["help_footer"],
        )

    def _get_cog_groups(self) -> list[str]:
        """
        Retrieves a list of cog groups from the 'modules' folder.

        Returns
        -------
        list[str]
            A list of cog groups.
        """
        cog_groups = sorted(
            [
                d
                for d in os.listdir("./modules")
                if Path(f"./modules/{d}").is_dir() and d not in ("__pycache__", "admin")
            ],
        )
        if "moderation" in cog_groups:
            cog_groups.remove("moderation")
            cog_groups.insert(0, "moderation")
        return cog_groups

    async def send_bot_help(
        self,
        mapping: Mapping[commands.Cog | None, list[commands.Command[Any, Any, Any]]],
    ) -> None:
        """
        Sends an overview of all commands in a single embed, grouped by module.

        Parameters
        ----------
        mapping : Mapping[commands.Cog | None, list[commands.Command[Any, Any, Any]]]
            The mapping of cogs to commands.
        """
        embed = self._embed_base("Luminara Help Overview")

        cog_groups = self._get_cog_groups()
        for group in cog_groups:
            group_commands: list[commands.Command[Any, Any, Any]] = []
            for cog, commands_list in mapping.items():
                if cog and commands_list and cog.__module__.startswith(f"modules.{group}"):
                    group_commands.extend(commands_list)
            if group_commands:
                command_list = ", ".join(f"`{c.name}`" for c in group_commands)
                embed.add_field(
                    name=group.capitalize(),
                    value=command_list,
                    inline=False,
                )

        await self.get_destination().send(embed=embed)

    async def _add_command_help_fields(
        self,
        embed: discord.Embed,
        command: commands.Command[Any, Any, Any],
    ) -> None:
        """
        Adds fields with usage and alias information for a command to an embed.

        Parameters
        ----------
        embed : discord.Embed
            The embed to which the fields will be added.
        command : commands.Command[Any, Any, Any]
            The command whose details are to be added.
        """
        prefix = await self._get_prefix()

        embed.add_field(
            name="Usage",
            value=f"`{prefix}{command.usage or 'No usage.'}`",
            inline=False,
        )

    async def send_command_help(self, command: commands.Command[Any, Any, Any]) -> None:
        """
        Sends a help message for a specific command.

        Parameters
        ----------
        command : commands.Command[Any, Any, Any]
            The command for which the help message is to be sent.
        """
        prefix = await self._get_prefix()

        author = f"{prefix}{command.qualified_name}"
        author += f" ({', '.join(command.aliases)})" if command.aliases else ""

        embed = self._embed_base(
            author=author,
            description=f"> {command.help}" or "No description available.",
        )

        await self._add_command_help_fields(embed, command)
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group: commands.Group[Any, Any, Any]) -> None:
        """
        Sends a help message for a specific command group.

        Parameters
        ----------
        group : commands.Group[Any, Any, Any]
            The group for which the help message is to be sent.
        """
        prefix = await self._get_prefix()
        embed = self._embed_base(
            author=f"{prefix}{group.qualified_name}",
            description=group.help or "No description available.",
        )

        for command in group.commands:
            embed.add_field(
                name=command.name,
                value=command.short_doc or "No description available.",
                inline=False,
            )

        await self.get_destination().send(embed=embed)

    async def send_error_message(self, error: str) -> None:
        """
        Sends an error message.

        Parameters
        ----------
        error : str
            The error message to be sent.
        """
        embed = Builder.create_embed(
            Builder.ERROR,
            title="Error in help command",
            description=error,
        )
        await self.get_destination().send(embed=embed, delete_after=30)
