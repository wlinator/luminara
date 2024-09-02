import asyncio
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import dropbox  # type: ignore
from discord.ext import commands, tasks
from dropbox.files import FileMetadata  # type: ignore
from loguru import logger

from lib.const import CONST

# Initialize Dropbox client if instance is "main"
_dbx: dropbox.Dropbox | None = None
if CONST.INSTANCE and CONST.INSTANCE.lower() == "main":
    _app_key: str | None = CONST.DBX_APP_KEY
    _dbx_token: str | None = CONST.DBX_TOKEN
    _app_secret: str | None = CONST.DBX_APP_SECRET

    _dbx = dropbox.Dropbox(
        app_key=_app_key,
        app_secret=_app_secret,
        oauth2_refresh_token=_dbx_token,
    )


def run_db_dump() -> None:
    command: str = (
        f"mariadb-dump --user={CONST.MARIADB_USER} --password={CONST.MARIADB_PASSWORD} "
        f"--host=db --single-transaction --all-databases > ./db/migrations/100-dump.sql"
    )
    subprocess.check_output(command, shell=True)


def upload_backup_to_dropbox(backup_name: str) -> None:
    with Path("./db/migrations/100-dump.sql").open("rb") as f:
        if _dbx:
            _dbx.files_upload(f.read(), f"/{backup_name}")  # type: ignore


async def create_db_backup() -> None:
    if not _dbx:
        msg = "Dropbox client is not initialized"
        raise ValueError(msg)

    backup_name: str = datetime.now(ZoneInfo("US/Eastern")).strftime("%Y-%m-%d_%H%M") + "_lumi.sql"

    run_db_dump()
    upload_backup_to_dropbox(backup_name)


async def backup_cleanup() -> None:
    if not _dbx:
        msg = "Dropbox client is not initialized"
        raise ValueError(msg)

    result = _dbx.files_list_folder("")  # type: ignore

    all_backup_files: list[str] = [entry.name for entry in result.entries if isinstance(entry, FileMetadata)]  # type: ignore

    for file in sorted(all_backup_files)[:-48]:
        _dbx.files_delete_v2(f"/{file}")  # type: ignore


async def backup() -> None:
    if CONST.INSTANCE and CONST.INSTANCE.lower() == "main":
        logger.debug("Backing up the database.")
        try:
            await create_db_backup()
            await backup_cleanup()
            logger.debug("Backup successful.")
        except Exception as error:
            logger.error(f"Backup failed: {error}")
    else:
        logger.debug('No backup, instance not "MAIN".')


class Backup(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.do_backup.start()

    @tasks.loop(hours=1)
    async def do_backup(self) -> None:
        await backup()

    @do_backup.before_loop
    async def before_do_backup(self) -> None:
        await self.bot.wait_until_ready()
        await asyncio.sleep(30)

    @commands.command()
    async def backup(self, ctx: commands.Context[commands.Bot]) -> None:
        await backup()
        await ctx.send("Backup successful.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Backup(bot))
