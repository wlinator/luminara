import discord
import textwrap

from config.parser import JsonCache

art = JsonCache.read_json("art")
hammer_icon = art["icons"]["hammer"]
cross_icon = art["icons"]["cross"]


def _clean_mod_embed():
    embed = discord.Embed(
        color=discord.Color.blurple()
    )

    return embed


def _clean_mod_error_embed(ctx):
    embed = discord.Embed(
        color=discord.Color.red(),
        description=f"**{ctx.author.name}** "
    )

    return embed


def shorten(text, width) -> str:
    return textwrap.shorten(text, width=width, placeholder="...")


class ModEmbeds:

    @staticmethod
    def user_banned(ctx, target_id, reason) -> discord.Embed:
        embed = _clean_mod_embed()
        embed.set_author(name="User Banned", icon_url=hammer_icon)

        embed.add_field(name="User ID", value=target_id, inline=False)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
        embed.add_field(name="Reason", value=shorten(reason, 37))

        return embed

    @staticmethod
    def member_banned(ctx, member_name, member_id, reason, dm_sent: bool) -> discord.Embed:
        embed = _clean_mod_embed()
        embed.set_author(name="Member Banned", icon_url=hammer_icon)

        embed.add_field(name="Username", value=member_name, inline=False)
        embed.add_field(name="User ID", value=member_id, inline=False)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
        embed.add_field(name="Reason", value=shorten(reason, 37))

        if not dm_sent:
            embed.set_footer(text="couldn't notify them in DM", icon_url=cross_icon)

        return embed

    @staticmethod
    def member_banned_dm(ctx, reason) -> discord.Embed:
        embed = discord.Embed(color=discord.Color.red())
        embed.set_author(name="Banned", icon_url=hammer_icon)
        embed.description = f"You were banned from **{ctx.guild.name}**."
        embed.add_field(name="Moderator", value=ctx.author.name, inline=False)
        embed.add_field(name="Reason", value=shorten(reason, 200), inline=False)

        return embed

    @staticmethod
    def user_unban(ctx, user_id):
        embed = _clean_mod_embed()
        embed.description = f"**{ctx.author.name}** you unbanned user with ID `{user_id}`."

        return embed


class ModErrors:
    @staticmethod
    def user_not_banned(ctx, user_id):
        embed = _clean_mod_error_embed(ctx)
        embed.description += f"user with ID `{user_id}` is not banned."

        return embed
