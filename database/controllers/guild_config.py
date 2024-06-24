from prisma.models import guild_config
from Client import db


class GuildConfigController:
    def __init__(self) -> None:
        self.table = db.guild_config

    async def get_prefix(self, guild_id: int) -> str:
        config: guild_config | None = await self.table.find_first(
            where={
                "guild_id": guild_id,
            }
        )

        return "." if not config or not config.prefix else config.prefix

    async def set_prefix(self, guild_id: int, prefix: str) -> None:
        await self.table.upsert(
            where={
                "guild_id": guild_id,
            },
            data={
                "update": {
                    "prefix": prefix,
                },
                "create": {
                    "guild_id": guild_id,
                    "prefix": prefix,
                },
            },
        )
