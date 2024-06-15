import logging
import os
import subprocess
from datetime import datetime

import dropbox

logs = logging.getLogger('Lumi.Core')

oauth2_refresh_token = os.environ.get("LUMI_DBX_OAUTH2_REFRESH_TOKEN")
app_key = os.environ.get("LUMI_DBX_APP_KEY")
app_secret = os.environ.get("LUMI_DBX_APP_SECRET")
instance = os.environ.get("LUMI_INSTANCE")
mariadb_user = os.environ.get("MARIADB_USER")
mariadb_password = os.environ.get("MARIADB_PASSWORD")

if instance.lower() == "main":
    dbx = dropbox.Dropbox(
        app_key=app_key,
        app_secret=app_secret,
        oauth2_refresh_token=oauth2_refresh_token
    )
else:
    # can be ignored
    dbx = None


async def create_db_backup(dbx, path="db/rcu.db"):
    backup_name = datetime.today().strftime('%Y-%m-%d_%H%M')
    backup_name += f"_lumi.sql"

    command = f"mariadb-dump --user={mariadb_user} --password={mariadb_password} " \
              f"--host=db --single-transaction --all-databases > ./db/init/2-data.sql"

    subprocess.check_output(command, shell=True)

    with open("./db/init/2-data.sql", "rb") as f:
        dbx.files_upload(f.read(), f"/{backup_name}")


async def backup_cleanup(dbx):
    all_backup_files = []

    for entry in dbx.files_list_folder('').entries:
        all_backup_files.append(entry.name)

    for file in sorted(all_backup_files[:-48]):
        dbx.files_delete_v2('/' + file)


async def backup(self):
    if instance.lower() == "main":
        try:
            await create_db_backup(dbx)
            await backup_cleanup(dbx)

            logs.info("[BACKUP] database backup success.")

        except Exception as error:
            logs.error(f"[BACKUP] database backup failed. {error}")
            logs.info(f"[BACKUP] Dropbox failure: {error}")
    else:
        logs.info("[BACKUP] No backup was made, instance not \"MAIN\".")
