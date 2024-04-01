import datetime

import discord

from services.Birthday import Birthday


async def cmd(ctx):
    upcoming_birthdays = Birthday.get_upcoming_birthdays(ctx.guild.id)
    icon = ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"

    embed = discord.Embed(
        color=discord.Color.embed_background()
    )
    embed.set_author(name="Upcoming Birthdays!", icon_url=icon)
    embed.set_thumbnail(url="https://i.imgur.com/79XfsbS.png")

    found_birthdays = 0
    for user_id, birthday in upcoming_birthdays:
        try:
            member = await ctx.guild.fetch_member(user_id)
            name = member.name
        except discord.HTTPException:
            continue  # skip user if not in guild

        try:
            birthday_date = datetime.datetime.strptime(birthday, "%m-%d")
            formatted_birthday = birthday_date.strftime("%B %-d")
        except ValueError:
            # leap year error
            formatted_birthday = "February 29"

        embed.add_field(
            name=f"{name}",
            value=f"🎂 {formatted_birthday}",
            inline=False
        )

        found_birthdays += 1
        if found_birthdays >= 5:
            break

    await ctx.respond(embed=embed)
