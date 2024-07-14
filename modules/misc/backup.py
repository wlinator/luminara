from loguru import logger
import os
import subprocess
from datetime import datetime
from typing import List, Optional

import dropbox
from dropbox.files import FileMetadata

# Fetch environment variables once and store them in constants
OAUTH2_REFRESH_TOKEN: Optional[str] = os.environ.get("LUMI_DBX_OAUTH2_REFRESH_TOKEN")
APP_KEY: Optional[str] = os.environ.get("LUMI_DBX_APP_KEY")
APP_SECRET: Optional[str] = os.environ.get("LUMI_DBX_APP_SECRET")
INSTANCE: Optional[str] = os.environ.get("LUMI_INSTANCE")
MARIADB_USER: Optional[str] = os.environ.get("MARIADB_USER")
MARIADB_PASSWORD: Optional[str] = os.environ.get("MARIADB_PASSWORD")

# Initialize Dropbox client if instance is "main"
_dbx: Optional[dropbox.Dropbox] = None
if INSTANCE and INSTANCE.lower() == "main":
    _dbx = dropbox.Dropbox(
        app_key=APP_KEY,
        app_secret=APP_SECRET,
        oauth2_refresh_token=OAUTH2_REFRESH_TOKEN
    )


async def create_db_backup() -> None:
    if not _dbx:
        raise ValueError("Dropbox client is not initialized")

    backup_name: str = datetime.today().strftime('%Y-%m-%d_%H%M') + "_lumi.sql"
    command: str = (
        f"mariadb-dump --user={MARIADB_USER} --password={MARIADB_PASSWORD} "
        f"--host=db --single-transaction --all-databases > ./db/migrations/100-dump.sql"
    )

    subprocess.check_output(command, shell=True)

    with open("./db/migrations/100-dump.sql", "rb") as f:
        _dbx.files_upload(f.read(), f"/{backup_name}")


async def backup_cleanup() -> None:
    if not _dbx:
        raise ValueError("Dropbox client is not initialized")

    result = _dbx.files_list_folder('')
    all_backup_files: List[str] = [
        entry.name for entry in result.entries if isinstance(entry, FileMetadata) # type: ignore
    ]

    for file in sorted(all_backup_files)[:-48]:
        _dbx.files_delete_v2('/' + file)


async def backup() -> None:
    if INSTANCE and INSTANCE.lower() == "main":
        logger.debug("Backing up the database.")
        try:
            await create_db_backup()
            await backup_cleanup()
            logger.debug("The database was backed up successfully.")
        except Exception as error:
            logger.error(f"Database backup failed. {error}")
    else:
        logger.debug("No backup was made, instance not \"MAIN\".")
