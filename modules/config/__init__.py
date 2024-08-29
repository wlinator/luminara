from discord.ext import commands

from modules.config.c_birthday import BirthdayConfig


class Config(BirthdayConfig, group_name="config"):
    pass


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Config(bot))
