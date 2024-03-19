import discord
from services.GuildConfig import GuildConfig


async def cmd(ctx):
    guild_config = GuildConfig(ctx.guild.id)

    embed = discord.Embed(
        color = discord.Color.embed_background(),
        title = f"{ctx.guild.name} configuration"
    )

    # birthdays
    if guild_config.birthday_channel_id:
        try:
            channel = ctx.guild.get_channel(guild_config.birthday_channel_id)
            birthday_config = f"Birthday announcements will be sent in {channel.mention}."

        except discord.HTTPException:
            birthday_config = f"The birthday channel seems to be invalid. Set it with `/config birthdays channel`."

    else:
        birthday_config = f"Birthdays are disabled, configure them with `/config birthdays channel`"

    embed.add_field(name="🎂 Birthdays", value=birthday_config, inline=False)


    # commands
    if guild_config.command_channel_id:
        try:
            channel = ctx.guild.get_channel(guild_config.command_channel_id)
            commands_config = f"XP and economy commands can only be used in {channel.mention}."

        except discord.HTTPException:
            commands_config = f"Commands can be used anywhere in the server."

    else:
        commands_config = f"Commands can be used anywhere in the server."

    embed.add_field(name="🤖 Commands", value=commands_config, inline=False)

    # greetings
    if guild_config.welcome_channel_id:
        try:
            channel = ctx.guild.get_channel(guild_config.welcome_channel_id)
            greeting_config = f"Welcome messages will be sent in {channel.mention}"

        except discord.HTTPException:
            greeting_config = f"The greeting channel seems to be invalid. Set it with `/config greetings channel`."

    else:
        greeting_config = f"Greetings are disabled, configure them with `/config greetings channel`"

    if guild_config.welcome_message:
        greeting_config += f"\nTemplate:\n```{guild_config.welcome_message}```"

    embed.add_field(name="👋 Greetings", value=greeting_config, inline=False)

    # levels
    if guild_config.level_message_type == 0:
        level_config = f"Levels are disabled in this server. Enable them with `/config levels enable`"

    elif guild_config.level_message_type == 1:
        level_config = f"levels are enabled and Racu will announce levels with __whimsical remarks__."

    else:
        level_config = f"levels are enabled and Racu will announce levels with a __generic message__."

    if guild_config.level_channel_id and guild_config.level_message_type != 0:
        try:
            channel = ctx.guild.get_channel(guild_config.level_channel_id)
            level_config += f"\nLevel announcements will always be sent in {channel.mention}."

        except discord.HTTPException:
            level_config += f"\nAnnouncements will be sent in the channel where the user levels up."

    else:
        if guild_config.level_message_type != 0:
            level_config += f"\nAnnouncements will be sent in the channel where the user levels up."

    if guild_config.level_message and guild_config.level_message_type == 2:
        level_config += f"\nTemplate:\n```{guild_config.level_message}```"

    embed.add_field(name="📈 Levels", value=level_config, inline=False)

    await ctx.respond(embed=embed)

