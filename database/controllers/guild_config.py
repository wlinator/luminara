from prisma.models import guild_config
from Client import db


class GuildConfigController:
    def __init__(self, guild_id) -> None:
        self.table = db.guild_config
        self.guild_id = guild_id

    async def get_prefix(self) -> str:
        config: guild_config | None = await self.table.find_first(
            where={
                "guild_id": self.guild_id,
            }
        )

        return "." if not config or not config.prefix else config.prefix

    async def set_prefix(self, prefix: str) -> None:
        await self.table.upsert(
            where={
                "guild_id": self.guild_id,
            },
            data={
                "update": {
                    "prefix": prefix,
                },
                "create": {
                    "guild_id": self.guild_id,
                    "prefix": prefix,
                },
            },
        )

    async def get_birthday_channel(self) -> int:
        config: guild_config | None = await self.table.find_first(
            where={
                "guild_id": self.guild_id,
            }
        )

        return (
            0
            if not config or not config.birthday_channel_id
            else config.birthday_channel_id
        )

    async def set_birthday_channel(self, guild_id: int, channel_id: int) -> None:
        await self.table.upsert(
            where={
                "guild_id": self.guild_id,
            },
            data={
                "update": {
                    "birthday_channel_id": channel_id,
                },
                "create": {
                    "guild_id": self.guild_id,
                    "birthday_channel_id": channel_id,
                },
            },
        )

    async def get_command_channel(self) -> int:
        config: guild_config | None = await self.table.find_first(
            where={
                "guild_id": self.guild_id,
            }
        )
        return (
            0
            if not config or not config.command_channel_id
            else config.command_channel_id
        )

    async def set_command_channel(self, channel_id: int) -> None:
        await self.table.upsert(
            where={
                "guild_id": self.guild_id,
            },
            data={
                "update": {
                    "command_channel_id": channel_id,
                },
                "create": {
                    "guild_id": self.guild_id,
                    "command_channel_id": channel_id,
                },
            },
        )

    async def get_intro_channel(self) -> int:
        config: guild_config | None = await self.table.find_first(
            where={
                "guild_id": self.guild_id,
            }
        )
        return (
            0 if not config or not config.intro_channel_id else config.intro_channel_id
        )

    async def set_intro_channel(self, channel_id: int) -> None:
        await self.table.upsert(
            where={
                "guild_id": self.guild_id,
            },
            data={
                "update": {
                    "intro_channel_id": channel_id,
                },
                "create": {
                    "guild_id": self.guild_id,
                    "intro_channel_id": channel_id,
                },
            },
        )

    async def get_welcome_channel(self) -> int:
        config: guild_config | None = await self.table.find_first(
            where={
                "guild_id": self.guild_id,
            }
        )
        return (
            0
            if not config or not config.welcome_channel_id
            else config.welcome_channel_id
        )

    async def set_welcome_channel(self, channel_id: int) -> None:
        await self.table.upsert(
            where={
                "guild_id": self.guild_id,
            },
            data={
                "update": {
                    "welcome_channel_id": channel_id,
                },
                "create": {
                    "guild_id": self.guild_id,
                    "welcome_channel_id": channel_id,
                },
            },
        )

    async def get_welcome_message(self) -> str:
        config: guild_config | None = await self.table.find_first(
            where={
                "guild_id": self.guild_id,
            }
        )
        return (
            "" if not config or not config.welcome_message else config.welcome_message
        )

    async def set_welcome_message(self, message: str) -> None:
        await self.table.upsert(
            where={
                "guild_id": self.guild_id,
            },
            data={
                "update": {
                    "welcome_message": message,
                },
                "create": {
                    "guild_id": self.guild_id,
                    "welcome_message": message,
                },
            },
        )

    async def get_boost_channel(self) -> int:
        config: guild_config | None = await self.table.find_first(
            where={
                "guild_id": self.guild_id,
            }
        )
        return (
            0 if not config or not config.boost_channel_id else config.boost_channel_id
        )

    async def set_boost_channel(self, channel_id: int) -> None:
        await self.table.upsert(
            where={
                "guild_id": self.guild_id,
            },
            data={
                "update": {
                    "boost_channel_id": channel_id,
                },
                "create": {
                    "guild_id": self.guild_id,
                    "boost_channel_id": channel_id,
                },
            },
        )

    async def get_boost_message(self) -> str:
        config: guild_config | None = await self.table.find_first(
            where={
                "guild_id": self.guild_id,
            }
        )
        return "" if not config or not config.boost_message else config.boost_message

    async def set_boost_message(self, message: str) -> None:
        await self.table.upsert(
            where={
                "guild_id": self.guild_id,
            },
            data={
                "update": {
                    "boost_message": message,
                },
                "create": {
                    "guild_id": self.guild_id,
                    "boost_message": message,
                },
            },
        )

    async def get_boost_image_url(self) -> str:
        config: guild_config | None = await self.table.find_first(
            where={
                "guild_id": self.guild_id,
            }
        )
        return (
            "" if not config or not config.boost_image_url else config.boost_image_url
        )

    async def set_boost_image_url(self, url: str) -> None:
        await self.table.upsert(
            where={
                "guild_id": self.guild_id,
            },
            data={
                "update": {
                    "boost_image_url": url,
                },
                "create": {
                    "guild_id": self.guild_id,
                    "boost_image_url": url,
                },
            },
        )

    async def get_level_channel(self) -> int:
        config: guild_config | None = await self.table.find_first(
            where={
                "guild_id": self.guild_id,
            }
        )
        return (
            0 if not config or not config.level_channel_id else config.level_channel_id
        )

    async def set_level_channel(self, channel_id: int) -> None:
        await self.table.upsert(
            where={
                "guild_id": self.guild_id,
            },
            data={
                "update": {
                    "level_channel_id": channel_id,
                },
                "create": {
                    "guild_id": self.guild_id,
                    "level_channel_id": channel_id,
                },
            },
        )

    async def get_level_message(self) -> str:
        config: guild_config | None = await self.table.find_first(
            where={
                "guild_id": self.guild_id,
            }
        )
        return "" if not config or not config.level_message else config.level_message

    async def set_level_message(self, message: str) -> None:
        await self.table.upsert(
            where={
                "guild_id": self.guild_id,
            },
            data={
                "update": {
                    "level_message": message,
                },
                "create": {
                    "guild_id": self.guild_id,
                    "level_message": message,
                },
            },
        )

    async def get_level_message_type(self) -> int:
        config: guild_config | None = await self.table.find_first(
            where={
                "guild_id": self.guild_id,
            }
        )
        return (
            1
            if not config or not config.level_message_type
            else config.level_message_type
        )

    async def set_level_message_type(self, message_type: int) -> None:
        await self.table.upsert(
            where={
                "guild_id": self.guild_id,
            },
            data={
                "update": {
                    "level_message_type": message_type,
                },
                "create": {
                    "guild_id": self.guild_id,
                    "level_message_type": message_type,
                },
            },
        )
