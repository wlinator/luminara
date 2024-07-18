from discord.ext import pages
from services.moderation.case_service import CaseService

case_service = CaseService()


async def view_case_by_number(ctx, guild_id: int, case_number: int):
    case = case_service.fetch_case_by_guild_and_number(guild_id, case_number)

    if not case:
        return await ctx.send("No case found with that ID.")

    await ctx.send(
        f"Case {case['case_number']}: {case['action_type']} - {case['reason']}",
    )


async def view_all_cases_in_guild(ctx, guild_id: int):
    cases = case_service.fetch_all_cases_in_guild(guild_id)

    if not cases:
        return await ctx.send("No cases found for this guild.")

    pages_list = [
        f"Case {case['case_number']}: {case['action_type']} - {case['reason']}"
        for case in cases
    ]
    paginator = pages.Paginator(pages=pages_list, loop_pages=True)
    await paginator.send(ctx)


async def view_all_cases_by_mod(ctx, guild_id: int, mod_id: int):
    cases = case_service.fetch_all_cases_by_mod(guild_id, mod_id)

    if not cases:
        return await ctx.send("No cases found for this moderator in this guild.")

    pages_list = [
        f"Case {case['case_number']}: {case['action_type']} - {case['reason']}"
        for case in cases
    ]
    paginator = pages.Paginator(pages=pages_list, loop_pages=True)
    await paginator.send(ctx)


async def edit_case_reason(ctx, guild_id: int, case_number: int, new_reason: str):
    changes = {"reason": new_reason}
    case_service.edit_case(guild_id, case_number, changes)
    await ctx.respond(f"Case {case_number} reason updated to: {new_reason}")


async def close_case(ctx, guild_id: int, case_number: int):
    case_service.close_case(guild_id, case_number)
    await ctx.respond(f"Case {case_number} has been closed.")
