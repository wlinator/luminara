import logging
import os
import discord
import platform

from discord.ext import bridge

logs = logging.getLogger('Racu.Core')


class RacuBot(bridge.Bot):
    async def on_ready(self):
        logs.info(f"[INFO] Logged in as {self.user.name} | {self.user.id}")
        logs.info(f"[INFO] discord.py API version: {discord.__version__}")
        logs.info(f"[INFO] Python version: {platform.python_version()}")
        logs.info(f"[INFO] Running on: {platform.system()} {platform.release()} ({os.name})")
        logs.info("-------------------------------------------------------")

        """
        https://docs.pycord.dev/en/stable/api/events.html#discord.on_ready
        This function isn't guaranteed to only be called once.
        Event is called when RESUME request fails.
        """

    @staticmethod
    async def get_or_fetch_channel(guild, channel_id):
        channel = guild.get_channel(channel_id)

        if not channel:
            try:
                channel = await guild.fetch_channel(channel_id)

            except (discord.HTTPException, discord.NotFound, discord.Forbidden):
                return None

        return channel

    @staticmethod
    async def get_or_fetch_member(guild, user_id):
        member = guild.get_member(user_id)

        if not member:
            try:
                member = await guild.fetch_member(user_id)

            except (discord.HTTPException, discord.NotFound, discord.Forbidden):
                return None

        return member
