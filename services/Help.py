import discord
from discord.ext import commands
from dotenv import load_dotenv

from config.parser import JsonCache
from lib.embeds.error import HelpErrors
import lib.checks

art = JsonCache.read_json("art")
load_dotenv('.env')


class RacuHelp(commands.HelpCommand):

    def __init__(self, **options):
        super().__init__(**options)
        self.verify_checks = True
        self.command_attrs = {
            "aliases": ["h"],
            "help": "Show a list of commands, or information about a specific command when an argument is passed.",
            "name": "help",
            "hidden": True
        }

    def get_command_qualified_name(self, command):
        return '`%s%s`' % (self.context.clean_prefix, command.qualified_name)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(color=discord.Color.blurple())

        embed.set_author(name="Help Command", icon_url=art["logo"]["transparent"])
        embed.description = (
            "Still need help? See [the wiki](https://wiki.wlinator.org/)!\n"
            "Bug reports & feature requests go [here](https://gitlab.com/wlinator/Racu/-/issues/new).\n\n"
            "Full list of commands: https://wiki.wlinator.org/cmdlist"
        )

        for cog, racu_commands in mapping.items():

            filtered = await self.filter_commands(racu_commands, sort=True)

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
        embed = discord.Embed(
            title=f"{self.context.clean_prefix}{command.qualified_name}",
            color=discord.Color.blurple(),
            description=command.help
        )

        usage_value = '`%s%s %s`' % (self.context.clean_prefix, command.qualified_name, command.signature)
        for alias in command.aliases:
            usage_value += '\n`%s%s %s`' % (self.context.clean_prefix, alias, command.signature)
        embed.add_field(name="Usage", value=usage_value, inline=False)

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

    async def command_callback(self, ctx, *, command=None):
        await self.prepare_help_command(ctx, command)
        bot = ctx.bot

        if command is None:
            mapping = self.get_bot_mapping()
            return await self.send_bot_help(mapping)

        # Check if it's a cog
        cog = bot.get_cog(command)
        if cog is not None:
            return await self.send_cog_help(cog)

        maybe_coro = discord.utils.maybe_coroutine

        # If it's not a cog then it's a command.
        # Since we want to have detailed errors when someone
        # passes an invalid subcommand, we need to walk through
        # the command group chain ourselves.
        keys = command.split(" ")

        cmd = bot.all_commands.get(keys[0].removeprefix(self.context.prefix))
        if cmd is None:
            string = await maybe_coro(
                self.command_not_found, self.remove_mentions(keys[0])
            )
            return await self.send_error_message(string)

        for key in keys[1:]:
            try:
                found = cmd.all_commands.get(key)
            except AttributeError:
                string = await maybe_coro(
                    self.subcommand_not_found, cmd, self.remove_mentions(key)
                )
                return await self.send_error_message(string)
            else:
                if found is None:
                    string = await maybe_coro(
                        self.subcommand_not_found, cmd, self.remove_mentions(key)
                    )
                    return await self.send_error_message(string)
                cmd = found

        return await self.send_command_help(cmd)
