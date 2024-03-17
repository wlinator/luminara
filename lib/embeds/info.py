import discord

question_icon = "https://i.imgur.com/8xccUws.png"
exclam_icon = "https://i.imgur.com/vitwMUu.png"


def clean_info_embed(ctx):
    embed = discord.Embed(
        color=discord.Color.brand_green(),
        description=f"**{ctx.author.name}** "
    )

    return embed


class EconInfo:
    @staticmethod
    def daily_reward_claimed(ctx, formatted_amount, streak):
        embed = clean_info_embed(ctx)
        embed.description += f"you claimed your reward of **${formatted_amount}**!"

        if streak > 1:
            embed.set_footer(text=f"You're on a streak of {streak} days",
                             icon_url=exclam_icon)

        return embed
