import discord
from discord.ext import commands
from lib.embeds.error import HelpErrors
from dotenv import load_dotenv
import os

load_dotenv('.env')

class RacuHelp(commands.HelpCommand):

    def __init__(self, **options):
        super().__init__(**options)
        self.verify_checks = False

    def get_command_signature(self, command):
        return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)

    def get_command_qualified_name(self, command):
        return '`%s%s`' % (self.context.clean_prefix, command.qualified_name)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(color=discord.Color.blurple())

        for cog, commands in mapping.items():

            if cog and cog.qualified_name.lower() == "admin" and int(os.getenv("OWNER_ID")) != self.context.author.id:
                continue

            filtered = await self.filter_commands(commands, sort=True)

            if command_signatures := [
                self.get_command_qualified_name(c) for c in filtered
            ]:
                # Remove duplicates using set() and convert back to a list
                unique_command_signatures = list(set(command_signatures))
                cog_name = getattr(cog, "qualified_name", "Help")
                embed.add_field(name=cog_name, value=", ".join(sorted(unique_command_signatures)), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=f"{self.context.clean_prefix}{command.qualified_name}",
                              color=discord.Color.blurple())
        if command.help:
            embed.description = command.help

        usage_value = '`%s%s %s`' % (self.context.clean_prefix, command.qualified_name, command.signature)

        for alias in command.aliases:
            usage_value += '\n`%s%s %s`' % (self.context.clean_prefix, alias, command.signature)

        embed.add_field(name="Usage", value=usage_value)
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_error_message(self, error):
        channel = self.get_destination()
        await channel.send(embed=HelpErrors.error_message(self.context, error))

    async def send_group_help(self, group):
        channel = self.get_destination()
        await channel.send(embed=HelpErrors.error_message(self.context,
                                                          f"No command called \"{group.qualified_name}\" found."))

    async def send_cog_help(self, cog):
        channel = self.get_destination()
        await channel.send(embed=HelpErrors.error_message(self.context,
                                                          f"No command called \"{cog.qualified_name}\" found."))
