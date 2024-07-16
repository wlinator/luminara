from lib.constants import CONST
from loguru import logger
import subprocess
from datetime import datetime
from typing import List, Optional

import dropbox
from dropbox.files import FileMetadata

# Initialize Dropbox client if instance is "main"
_dbx: Optional[dropbox.Dropbox] = None
if CONST.INSTANCE and CONST.INSTANCE.lower() == "main":
    _app_key: Optional[str] = CONST.DBX_APP_KEY
    _dbx_token: Optional[str] = CONST.DBX_TOKEN
    _app_secret: Optional[str] = CONST.DBX_APP_SECRET

    _dbx = dropbox.Dropbox(
        app_key=_app_key,
        app_secret=_app_secret,
        oauth2_refresh_token=_dbx_token,
    )


async def create_db_backup() -> None:
    if not _dbx:
        raise ValueError("Dropbox client is not initialized")

    backup_name: str = datetime.today().strftime("%Y-%m-%d_%H%M") + "_lumi.sql"
    command: str = (
        f"mariadb-dump --user={CONST.MARIADB_USER} --password={CONST.MARIADB_PASSWORD} "
        f"--host=db --single-transaction --all-databases > ./db/migrations/100-dump.sql"
    )

    subprocess.check_output(command, shell=True)

    with open("./db/migrations/100-dump.sql", "rb") as f:
        _dbx.files_upload(f.read(), f"/{backup_name}")


async def backup_cleanup() -> None:
    if not _dbx:
        raise ValueError("Dropbox client is not initialized")

    result = _dbx.files_list_folder("")

    all_backup_files: List[str] = [
        entry.name
        for entry in result.entries
        if isinstance(entry, FileMetadata)  # type: ignore
    ]

    for file in sorted(all_backup_files)[:-48]:
        _dbx.files_delete_v2("/" + file)


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
