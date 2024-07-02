import discord

from config.parser import JsonCache
from services.config_service import GuildConfig

strings = JsonCache.read_json("strings")


async def cmd(self, ctx):
    guild_config = GuildConfig(ctx.guild.id)

    embed = discord.Embed(
        color=discord.Color.embed_background(),
        description="Guide: https://wiki.wlinator.org/serverconfig",
    )
    icon = ctx.guild.icon if ctx.guild.icon else "https://i.imgur.com/79XfsbS.png"
    embed.set_author(name=f"{ctx.guild.name} config", icon_url=icon)

    # birthdays
    if guild_config.birthday_channel_id:
        channel = await self.client.get_or_fetch_channel(
            ctx.guild, guild_config.birthday_channel_id
        )

        if channel:
            birthday_config = f"✅ | in {channel.mention}."
        else:
            birthday_config = "❌ | enable the module with `/config birthdays channel`"

    else:
        birthday_config = "❌ | enable the module with `/config birthdays channel`"

    embed.add_field(name="BIRTHDAYS", value=birthday_config, inline=False)

    # commands
    if guild_config.command_channel_id:
        channel = await self.client.get_or_fetch_channel(
            ctx.guild, guild_config.command_channel_id
        )

        if channel:
            commands_config = f"✅ | commands only allowed in {channel.mention}."
        else:
            commands_config = "✅ | commands allowed anywhere."
    else:
        commands_config = "✅ | commands allowed anywhere."

    embed.add_field(name="COMMANDS", value=commands_config, inline=False)

    # greetings
    if guild_config.welcome_channel_id:
        channel = await self.client.get_or_fetch_channel(
            ctx.guild, guild_config.welcome_channel_id
        )

        if channel:
            greeting_config = f"✅ | in {channel.mention}"

            if guild_config.welcome_message:
                greeting_config += (
                    f" with template:\n```{guild_config.welcome_message}```"
                )
            else:
                greeting_config += " without custom template."

        else:
            greeting_config = "❌ | enable the module with `/config greetings channel`"
    else:
        greeting_config = "❌ | enable the module with `/config greetings channel`"

    embed.add_field(name="GREETINGS", value=greeting_config, inline=False)

    # boosts
    if guild_config.boost_channel_id:
        channel = await self.client.get_or_fetch_channel(
            ctx.guild, guild_config.boost_channel_id
        )

        if channel:
            boost_config = f"✅ | in {channel.mention}"

            if guild_config.boost_message:
                if guild_config.boost_image_url:
                    boost_config += f" with custom image and template:\n```{guild_config.boost_message}```"
                else:
                    boost_config += (
                        f" with custom template:\n```{guild_config.boost_message}```"
                    )
            else:
                if guild_config.boost_image_url:
                    boost_config += " with custom image, but no template."
                else:
                    boost_config += " without custom image or template."

        else:
            boost_config = "❌ | enable the module with `/config boosts channel`"
    else:
        boost_config = "❌ | enable the module with `/config boosts channel`"

    embed.add_field(name="BOOSTS", value=boost_config, inline=False)

    # levels
    if guild_config.level_message_type == 0:
        level_config = "❌ | enable levels with `/config levels enable`"

    elif guild_config.level_message_type == 1:
        level_config = "✅ | whimsical/sarcastic announcements"

    else:
        level_config = "✅ | generic announcements"

    if guild_config.level_channel_id and guild_config.level_message_type != 0:
        channel = await self.client.get_or_fetch_channel(
            ctx.guild, guild_config.level_channel_id
        )

        if channel:
            level_config += f" in {channel.mention}"
        else:
            level_config += " in the user's current channel"

    else:
        if guild_config.level_message_type != 0:
            level_config += " in the user's current channel"

    if guild_config.level_message and guild_config.level_message_type == 2:
        level_config += f" with template:\n```{guild_config.level_message}```"
    if not guild_config.level_message and guild_config.level_message_type == 2:
        level_config += f" with template:\n```{strings['level_up']}```"

    embed.add_field(name="LEVELS", value=level_config, inline=False)

    await ctx.respond(embed=embed)
