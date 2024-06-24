from prisma.models import guild_config
from Client import db


class GuildConfigController:
    def __init__(self) -> None:
        self.table = db.guild_config

    async def _create_config_if_not_exist(self, guild_id: int) -> None:
        config = await self.table.find_first(guild_config.guild_id == guild_id)

        if not config:
            await self.table.create(
                data={"guild_id": guild_id},
            )

    async def get_prefix(self, guild_id: int) -> str:
        config: guild_config | None = await self.table.find_first(
            guild_config.guild_id == guild_id
        )

        return "." if not config or not config.prefix else config.prefix
