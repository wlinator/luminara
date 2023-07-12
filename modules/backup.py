import logging
import os
from datetime import datetime

import dropbox.files
from discord.ext import commands, tasks
from dotenv import load_dotenv

racu_logs = logging.getLogger('Racu.Core')
load_dotenv('.env')

dropbox_token = os.getenv("DROPBOX_TOKEN")
instance = os.getenv("INSTANCE")


async def create_db_backup(dbx, path="db/rcu.db"):
    backup_name = datetime.today().strftime('%Y-%m-%d_%H%M')
    backup_name += f"_racu.db"

    with open(path, "rb") as f:
        data = f.read()
        dbx.files_upload(data, f"/{backup_name}")


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
                dbx = dropbox.Dropbox(dropbox_token)

                await create_db_backup(dbx)
                await backup_cleanup(dbx)

                racu_logs.info("DB Dropbox backup success.")

            except Exception as error:
                racu_logs.error("DB Dropbox backup failed.")
                racu_logs.debug(f"Dropbox failure: {error}")
        else:
            racu_logs.info("No backup was made, instance not \"MAIN\".")


def setup(sbbot):
    sbbot.add_cog(BackupCog(sbbot))
