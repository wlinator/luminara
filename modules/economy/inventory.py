import discord

from services.Inventory import Inventory


async def cmd(ctx):
    inventory = Inventory(ctx.author.id)
    inventory_dict = inventory.get_inventory()

    description = "You don't have any items!" if inventory_dict == {} else None

    embed = discord.Embed(
        color=discord.Color.embed_background(),
        description=description
    )
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)

    for item, quantity in inventory_dict.items():
        if item.type == "badge":

            if not embed.description:
                embed.description = "**Badges:** "

            emote = self.client.get_emoji(item.emote_id)
            embed.description += f"{emote} "

        else:
            emote = self.client.get_emoji(item.emote_id)
            embed.add_field(name=f"{emote} {item.display_name.capitalize()}",
                            value=f"*— amount: `{quantity}`*",
                            inline=False)

    await ctx.respond(embed=embed)
