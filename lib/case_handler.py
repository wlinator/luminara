import discord
from discord.ext import commands
from loguru import logger

from lib.client import Luminara
from lib.exceptions import LumiException
from services.case_service import CaseService
from services.modlog_service import ModLogService
from ui.cases import create_case_embed

case_service = CaseService()
modlog_service = ModLogService()


async def create_case(
    ctx: commands.Context[Luminara],
    target: discord.User,
    action_type: str,
    reason: str | None = None,
    duration: int | None = None,
    expires_at: str | None = None,
):
    """
    Creates a new moderation case and logs it to the modlog channel if configured.

    Args:
        ctx: The context of the command invocation.
        target (discord.User): The user who is the subject of the moderation action.
        action_type (str): The type of moderation action (e.g., "ban", "kick", "warn").
        reason (Optional[str]): The reason for the moderation action. Defaults to None.
        duration (Optional[int]): The duration of the action in seconds, if applicable. Defaults to None.
        expires_at (Optional[str]): The expiration date of the action, if applicable. Defaults to None.

    Returns:
        None

    Raises:
        Exception: If there's an error sending the case to the modlog channel.

    This function performs the following steps:
    1. Creates a new case in the database using the CaseService.
    2. Logs the case creation using the logger.
    3. If a modlog channel is configured, it sends an embed with the case details to that channel.
    4. If the embed is successfully sent to the modlog channel, it updates the case with the message ID for later edits.
    """

    if not ctx.guild:
        raise LumiException

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

    if mod_log_channel_id := modlog_service.fetch_modlog_channel_id(guild_id):
        try:
            mod_log_channel = await commands.TextChannelConverter().convert(
                ctx,
                str(mod_log_channel_id),
            )
            embed: discord.Embed = create_case_embed(
                ctx=ctx,
                target=target,
                case_number=case_number,
                action_type=action_type,
                reason=reason,
                timestamp=None,
                duration=duration,
            )
            message = await mod_log_channel.send(embed=embed)

            # Update the case with the modlog_message_id
            case_service.edit_case(
                guild_id=guild_id,
                case_number=case_number,
                changes={"modlog_message_id": message.id},
            )

        except Exception as e:
            logger.error(f"Failed to send case to modlog channel: {e}")


async def edit_case_modlog(
    ctx: commands.Context[Luminara],
    guild_id: int,
    case_number: int,
    new_reason: str,
) -> bool:
    """
    Edits the reason for an existing case and updates the modlog message if it exists.

    Args:
        ctx: The context of the command invocation.
        guild_id: The ID of the guild where the case exists.
        case_number: The number of the case to edit.
        new_reason: The new reason for the case.

    Raises:
        ValueError: If the case is not found.
        Exception: If there's an error updating the modlog message.
    """
    case = case_service.fetch_case_by_guild_and_number(guild_id, case_number)
    if not case:
        msg = f"Case {case_number} not found in guild {guild_id}"
        raise ValueError(msg)

    modlog_message_id = case.get("modlog_message_id")
    if not modlog_message_id:
        return False

    mod_log_channel_id = modlog_service.fetch_modlog_channel_id(guild_id)
    if not mod_log_channel_id:
        return False

    try:
        mod_log_channel = await commands.TextChannelConverter().convert(
            ctx,
            str(mod_log_channel_id),
        )
        message = await mod_log_channel.fetch_message(modlog_message_id)
        target = await commands.UserConverter().convert(ctx, str(case["target_id"]))

        updated_embed: discord.Embed = create_case_embed(
            ctx=ctx,
            target=target,
            case_number=case_number,
            action_type=case["action_type"],
            reason=new_reason,
            timestamp=case["created_at"],
            duration=case["duration"] or None,
        )

        await message.edit(embed=updated_embed)
        logger.info(f"Updated case {case_number} in guild {guild_id}")

    except Exception as e:
        logger.error(f"Failed to update modlog message for case {case_number}: {e}")
        return False

    return True
