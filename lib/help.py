from collections.abc import Mapping
from typing import Any

from discord.ext import commands

from lib.const import CONST
from lib.exceptions import LumiException
from ui.embeds import Builder


class LumiHelp(commands.HelpCommand):
    def __init__(self, **options: Any) -> None:
        super().__init__(**options)
        self.verify_checks: bool = True
        self.command_attrs: dict[str, list[str] | str | bool] = {
            "aliases": ["h"],
            "help": "Show a list of commands, or information about a specific command when an argument is passed.",
            "name": "help",
            "hidden": True,
        }

    def get_command_qualified_name(self, command: commands.Command[Any, Any, Any]) -> str:
        return f"`{self.context.clean_prefix}{command.qualified_name}`"

    async def send_bot_help(self, mapping: Mapping[commands.Cog | None, list[commands.Command[Any, ..., Any]]]) -> None:
        embed = Builder.create_embed(
            theme="success",
            author_text="Help Command",
            user_name=self.context.author.name,
            hide_name_in_description=True,
        )

        for cog, lumi_commands in mapping.items():
            filtered: list[commands.Command[Any, Any, Any]] = await self.filter_commands(lumi_commands, sort=True)

            if command_signatures := [self.get_command_qualified_name(c) for c in filtered]:
                # Remove duplicates using set() and convert back to a list
                unique_command_signatures: list[str] = list(set(command_signatures))
                cog_name: str = getattr(cog, "qualified_name", "Help")
                embed.add_field(
                    name=cog_name,
                    value=", ".join(sorted(unique_command_signatures)),
                    inline=False,
                )

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command: commands.Command[Any, Any, Any]) -> None:
        embed = Builder.create_embed(
            theme="success",
            author_text=f"{self.context.clean_prefix}{command.qualified_name}",
            description=command.description,
            user_name=self.context.author.name,
            hide_name_in_description=True,
        )

        usage_value: str = f"`{self.context.clean_prefix}{command.usage}`"
        embed.add_field(name="Usage", value=usage_value, inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_error_message(self, error: str) -> None:
        raise LumiException(error)

    async def send_group_help(self, group: commands.Group[Any, Any, Any]) -> None:
        raise LumiException(
            CONST.STRINGS["error_command_not_found"].format(group.qualified_name),
        )

    async def send_cog_help(self, cog: commands.Cog) -> None:
        raise LumiException(
            CONST.STRINGS["error_command_not_found"].format(cog.qualified_name),
        )
