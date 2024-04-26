# noinspection PyInterpreter
import logging

from discord.ext.commands import Cog

from lib.embeds.greet import Greet
from services.GuildConfig import GuildConfig

_logs = logging.getLogger('Racu.Core')


class EventHandler(Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_member_join(self, member):
        config = GuildConfig(member.guild.id)

        if not config.welcome_channel_id:
            return

        embed = Greet.message(member, config.welcome_message)

        try:
            await member.guild.get_channel(config.welcome_channel_id).send(embed=embed, content=member.mention)
        except Exception as e:
            _logs.info(f"[GreetingHandler] Message not sent in '{member.guild.name}'. Channel ID may be invalid. {e}")

    # @Cog.listener()
    # async def on_member_update(self, before, after):
    #     config = GuildConfig(after.guild.id)
    #
    #     if not config.boost_channel_id:
    #         return

    @Cog.listener()
    async def on_command_completion(self, ctx) -> None:
        log_msg = '[CommandHandler] %s executed .%s | PREFIX' % (ctx.author.name, ctx.command.qualified_name)

        if ctx.guild is not None:
            _logs.info(f"{log_msg} | guild: {ctx.guild.name} ")
        else:
            _logs.info(f"{log_msg} | in DMs")

    @Cog.listener()
    async def on_application_command_completion(self, ctx) -> None:
        log_msg = '[CommandHandler] %s executed /%s | SLASH' % (ctx.author.name, ctx.command.qualified_name)

        if ctx.guild is not None:
            _logs.info(f"{log_msg} | guild: {ctx.guild.name} ")
        else:
            _logs.info(f"{log_msg} | in DMs")


def setup(client):
    client.add_cog(EventHandler(client))
