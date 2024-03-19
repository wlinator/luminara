import discord
from services.GuildConfig import GuildConfig
from main import strings


async def cmd(ctx):
    guild_config = GuildConfig(ctx.guild.id)

    embed = discord.Embed(
        color = discord.Color.embed_background(),
        description = f"Due to the complexity of the config system, "
                      f"changes can only be made with slash commands."
    )
    icon = ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
    embed.set_author(name=f"{ctx.guild.name} config", icon_url=icon)

    # birthdays
    if guild_config.birthday_channel_id:
        try:
            channel = ctx.guild.get_channel(guild_config.birthday_channel_id)
            birthday_config = f"✅ | in {channel.mention}."
        except discord.HTTPException:
            birthday_config = f"❌ | enable the module with `/config birthdays channel`"
    else:
        birthday_config = f"❌ | enable the module with `/config birthdays channel`"

    embed.add_field(name="BIRTHDAYS", value=birthday_config, inline=False)

    # commands
    if guild_config.command_channel_id:
        try:
            channel = ctx.guild.get_channel(guild_config.command_channel_id)
            commands_config = f"✅ | commands only allowed in {channel.mention}."
        except discord.HTTPException:
            commands_config = f"✅ | commands allowed anywhere."
    else:
        commands_config = f"✅ | commands allowed anywhere."

    embed.add_field(name="COMMANDS", value=commands_config, inline=False)

    # greetings
    if guild_config.welcome_channel_id:
        try:
            channel = ctx.guild.get_channel(guild_config.welcome_channel_id)
            greeting_config = f"✅ | in {channel.mention}"

            if guild_config.welcome_message:
                greeting_config += f" with template:\n```{guild_config.welcome_message}```"
            else:
                greeting_config += f" without custom template."

        except discord.HTTPException:
            greeting_config = f"❌ | enable the module with `/config greetings channel`"
    else:
        greeting_config = f"❌ | enable the module with `/config greetings channel`"

    embed.add_field(name="GREETINGS", value=greeting_config, inline=False)

    # levels
    if guild_config.level_message_type == 0:
        level_config = f"❌ | enable levels with `/config levels enable`"

    elif guild_config.level_message_type == 1:
        level_config = f"✅ | whimsical/sarcastic announcements"

    else:
        level_config = f"✅ | generic announcements"

    if guild_config.level_channel_id and guild_config.level_message_type != 0:
        try:
            channel = ctx.guild.get_channel(guild_config.level_channel_id)
            level_config += f" in {channel.mention}"

        except discord.HTTPException:
            level_config += f" in the user's current channel"

    else:
        if guild_config.level_message_type != 0:
            level_config += f" in the user's current channel"

    if guild_config.level_message and guild_config.level_message_type == 2:
        level_config += f" with template:\n```{guild_config.level_message}```"
    if not guild_config.level_message and guild_config.level_message_type == 2:
        level_config += f" with template:\n```{strings['level_up']}```"

    embed.add_field(name="LEVELS", value=level_config, inline=False)

    await ctx.respond(embed=embed)

