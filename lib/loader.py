from loguru import logger
from discord.ext import commands
from lib.const import CONST
from pathlib import Path
import aiofiles.os


class CogLoader(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cog_ignore_list: set[str] = CONST.COG_IGNORE_LIST

    async def is_cog(self, path: Path) -> bool:
        cog_name: str = path.stem

        if cog_name in self.cog_ignore_list:
            logger.debug(f"Ignoring cog: {cog_name} because it is in the ignore list")
            return False

        return (
            path.suffix == ".py"
            and not path.name.startswith("_")
            and await aiofiles.os.path.isfile(path)
        )

    async def load_cogs(self, path: Path) -> None:
        try:
            if await aiofiles.os.path.isdir(path):
                for item in path.iterdir():
                    try:
                        await self.load_cogs(path=item)
                    except Exception as e:
                        logger.exception(f"Error loading cog from {item}: {e}")

            elif await self.is_cog(path):
                relative_path: Path = path.relative_to(Path(__file__).parent.parent)
                module: str = (
                    str(relative_path).replace("/", ".").replace("\\", ".")[:-3]
                )
                try:
                    await self.bot.load_extension(name=module)
                    logger.debug(f"Loaded cog: {module}")

                except Exception as e:
                    logger.exception(f"Error loading cog: {module}. Error: {e}")

        except Exception as e:
            logger.exception(f"Error loading cogs from {path}: {e}")

    async def load_cog_from_dir(self, dir_name: str) -> None:
        path: Path = Path(__file__).parent.parent / dir_name
        await self.load_cogs(path)

    @classmethod
    async def setup(cls, bot: commands.Bot) -> None:
        cog_loader = cls(bot)
        await cog_loader.load_cog_from_dir(dir_name="modules")
        await cog_loader.load_cog_from_dir(dir_name="handlers")
        await bot.add_cog(cog_loader)
