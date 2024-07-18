import discord
from loguru import logger
from services.moderation.case_service import CaseService
from services.moderation.modlog_service import ModLogService
from modules.moderation.utils.case_embed import create_case_embed
from typing import Optional
from discord.ext.commands import TextChannelConverter

case_service = CaseService()
modlog_service = ModLogService()


async def create_case(
    ctx,
    target: discord.User,
    action_type: str,
    reason: Optional[str] = None,
    duration: Optional[int] = None,
    expires_at: Optional[str] = None,
):
    guild_id = ctx.guild.id
    moderator_id = ctx.author.id
    target_id = target.id

    # Create the case
    case_number: int = case_service.create_case(
        guild_id=guild_id,
        target_id=target_id,
        moderator_id=moderator_id,
        action_type=action_type,
        reason=reason,
        duration=duration,
        expires_at=expires_at,
        modlog_message_id=None,
    )

    logger.info(f"Created case {case_number} for {target.name} in guild {guild_id}")

    # Send the case to the modlog if configured
    mod_log_channel_id = modlog_service.fetch_modlog_channel_id(guild_id)

    if mod_log_channel_id:
        try:
            mod_log_channel = await TextChannelConverter().convert(
                ctx,
                str(mod_log_channel_id),
            )
            embed = create_case_embed(ctx, target, case_number, action_type, reason)
            message = await mod_log_channel.send(embed=embed)

            # Update the case with the modlog_message_id
            case_service.edit_case(
                guild_id=guild_id,
                case_number=case_number,
                changes={"modlog_message_id": message.id},
            )

        except Exception as e:
            logger.error(f"Failed to send case to modlog channel: {e}")
