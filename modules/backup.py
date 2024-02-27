import logging
import os
import subprocess
from datetime import datetime

import dropbox
from discord.ext import commands, tasks
from dotenv import load_dotenv

racu_logs = logging.getLogger('Racu.Core')
load_dotenv('.env')

oauth2_refresh_token = os.getenv("DBX_OAUTH2_REFRESH_TOKEN")
app_key = os.getenv("DBX_APP_KEY")
app_secret = os.getenv("DBX_APP_SECRET")
instance = os.getenv("INSTANCE")
mariadb_user = os.getenv("MARIADB_USER")
mariadb_password = os.getenv("MARIADB_PASSWORD")

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
    backup_name += f"_racu.sql"

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


class BackupCog(commands.Cog):
    def __init__(self, sbbot):
        self.bot = sbbot
        self.do_backup.start()

    @tasks.loop(hours=1)
    async def do_backup(self):

        if instance.lower() == "main":
            try:
                await create_db_backup(dbx)
                await backup_cleanup(dbx)

                racu_logs.info("DB Dropbox backup success.")

            except Exception as error:
                racu_logs.error(f"DB Dropbox backup failed. {error}")
                racu_logs.debug(f"Dropbox failure: {error}")
        else:
            racu_logs.info("No backup was made, instance not \"MAIN\".")


def setup(sbbot):
    sbbot.add_cog(BackupCog(sbbot))
