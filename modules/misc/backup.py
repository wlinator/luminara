from loguru import logger
import os
import subprocess
from datetime import datetime

import dropbox

oauth2_refresh_token = os.environ.get("LUMI_DBX_OAUTH2_REFRESH_TOKEN")
app_key = os.environ.get("LUMI_DBX_APP_KEY")
app_secret = os.environ.get("LUMI_DBX_APP_SECRET")
instance = os.environ.get("LUMI_INSTANCE")
mariadb_user = os.environ.get("MARIADB_USER")
mariadb_password = os.environ.get("MARIADB_PASSWORD")

if instance.lower() == "main":
    _dbx = dropbox.Dropbox(
        app_key=app_key,
        app_secret=app_secret,
        oauth2_refresh_token=oauth2_refresh_token
    )
else:
    # can be ignored
    _dbx = None


async def create_db_backup():
    backup_name = datetime.today().strftime('%Y-%m-%d_%H%M')
    backup_name += f"_lumi.sql"

    command = f"mariadb-dump --user={mariadb_user} --password={mariadb_password} " \
              f"--host=db --single-transaction --all-databases > ./db/migrations/100-dump.sql"

    subprocess.check_output(command, shell=True)

    with open("./db/migrations/100-dump.sql", "rb") as f:
        _dbx.files_upload(f.read(), f"/{backup_name}")


async def backup_cleanup():
    all_backup_files = []

    for entry in _dbx.files_list_folder('').entries:
        all_backup_files.append(entry.name)

    for file in sorted(all_backup_files[:-48]):
        _dbx.files_delete_v2('/' + file)


async def backup():
    if instance.lower() == "main":
        logger.debug("Backing up the database.")
        try:
            await create_db_backup()
            await backup_cleanup()

            logger.debug("The database was backed up successfully.")

        except Exception as error:
            logger.error(f"database backup failed. {error}")
    else:
        logger.debug("No backup was made, instance not \"MAIN\".")
