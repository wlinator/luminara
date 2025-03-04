from datetime import datetime

from discord.ext import commands

import lib.format
from lib.client import Luminara
from lib.const import CONST
from lib.exceptions import LumiException
from services.rooster_service import RoosterService
from ui.embeds import Builder


class Rooster(commands.Cog):
    def __init__(self, bot: Luminara) -> None:
        self.bot: Luminara = bot
        self.myrooster.usage = lib.format.generate_usage(self.myrooster)
        self.newrooster.usage = lib.format.generate_usage(self.newrooster)
        self.train.usage = lib.format.generate_usage(self.train)

    @commands.hybrid_command(
        name="rooster",
        aliases=["cock"],
    )
    @commands.guild_only()
    async def myrooster(  # noqa: PLR0912, PLR0915
        self,
        ctx: commands.Context[Luminara],
    ) -> None:
        """
        View your rooster's information, level, achievements, campaign progress, and items.

        Parameters
        ----------
        ctx : commands.Context[Luminara]
            The context of the command.
        """
        rooster_service = RoosterService(ctx.author.id)

        if not rooster_service.has_rooster():
            embed = Builder.create_embed(
                Builder.ERROR,
                user_name=ctx.author.name,
                author_text=CONST.STRINGS["rooster_no_rooster_author"],
                description=CONST.STRINGS["rooster_no_rooster"],
            )
            await ctx.send(embed=embed)
            return

        rooster = rooster_service.rooster
        if rooster is None:
            # This should not happen since we checked has_rooster() above
            return

        equipment = rooster_service.get_rooster_equipment()
        inventory = rooster_service.get_user_items()
        campaigns = rooster_service.get_campaign_progress()
        achievements = rooster_service.get_achievements()

        # Create embed
        embed = Builder.create_embed(
            Builder.SUCCESS,
            user_name=ctx.author.name,
            author_text=CONST.STRINGS["rooster_info_author"].format(ctx.author.name),
            author_icon_url=ctx.author.display_avatar.url,
            description=CONST.STRINGS["rooster_info_description"].format(
                rooster["level"],
                rooster["xp"],
                rooster["xp_needed"],
                rooster["wins"],
                rooster["losses"],
            ),
            hide_name_in_description=True,
            hide_time=True,
        )

        # Stats section
        embed.add_field(
            name=CONST.STRINGS["rooster_stats_title"],
            value=CONST.STRINGS["rooster_stats_value"].format(
                rooster["strength"],
                rooster["agility"],
                rooster["endurance"],
                rooster["technique"],
                rooster["luck"],
            ),
            inline=True,
        )

        # Equipment section
        equipment_text = ""
        if equipment:
            equipment_items = [
                ("Head", "head_name", "head_rarity"),
                ("Body", "body_name", "body_rarity"),
                ("Legs", "leg_name", "leg_rarity"),
                ("Spurs", "spur_name", "spur_rarity"),
                ("Talisman", "talisman_name", "talisman_rarity"),
            ]

            for slot_name, name_key, rarity_key in equipment_items:
                if equipment.get(name_key):
                    equipment_text += (
                        CONST.STRINGS["rooster_equipment_item"].format(
                            slot_name,
                            equipment[name_key],
                            RoosterService.format_rarity(equipment[rarity_key]),
                        )
                        + "\n"
                    )
                else:
                    equipment_text += CONST.STRINGS["rooster_equipment_empty"].format(slot_name) + "\n"
        else:
            equipment_text = CONST.STRINGS["rooster_equipment_none"]

        embed.add_field(name=CONST.STRINGS["rooster_equipment_title"], value=equipment_text.strip(), inline=True)

        # Inventory section
        if inventory:
            inventory_text = "\n".join(
                [
                    CONST.STRINGS["rooster_inventory_item"].format(
                        item["name"],
                        RoosterService.format_rarity(item["rarity"]),
                        item["quantity"],
                    )
                    for item in inventory[:5]
                ],
            )

            if len(inventory) > 5:
                inventory_text += "\n" + CONST.STRINGS["rooster_inventory_more"].format(len(inventory) - 5)
        else:
            inventory_text = CONST.STRINGS["rooster_inventory_none"]

        embed.add_field(name=CONST.STRINGS["rooster_inventory_title"], value=inventory_text, inline=False)

        # Campaign progress section
        if campaigns:
            campaign_text = "\n".join(
                [
                    CONST.STRINGS["rooster_campaign_item"].format(
                        campaign["name"],
                        RoosterService.format_difficulty(campaign["difficulty"]),
                        CONST.STRINGS["rooster_campaign_completed"]
                        if campaign["completed"]
                        else CONST.STRINGS["rooster_campaign_not_completed"],
                        campaign["attempts"],
                    )
                    for campaign in campaigns[:3]
                ],
            )

            if len(campaigns) > 3:
                campaign_text += "\n" + CONST.STRINGS["rooster_campaign_more"].format(len(campaigns) - 3)
        else:
            campaign_text = CONST.STRINGS["rooster_campaign_none"]

        embed.add_field(name=CONST.STRINGS["rooster_campaign_title"], value=campaign_text, inline=False)

        # Achievements section
        if achievements:
            unlocked_achievements = [a for a in achievements if a["unlocked"]]
            if unlocked_achievements:
                achievement_text = "\n".join(
                    [
                        CONST.STRINGS["rooster_achievements_item"].format(achievement["name"])
                        for achievement in unlocked_achievements[:3]
                    ],
                )

                if len(unlocked_achievements) > 3:
                    achievement_text += "\n" + CONST.STRINGS["rooster_achievements_more"].format(
                        len(unlocked_achievements) - 3,
                    )
            else:
                achievement_text = CONST.STRINGS["rooster_achievements_none"]
        else:
            achievement_text = CONST.STRINGS["rooster_achievements_none"]

        embed.add_field(name=CONST.STRINGS["rooster_achievements_title"], value=achievement_text, inline=False)

        # Add footer with creation date
        created_at = rooster["created_at"]
        created_at_str = created_at.strftime("%Y-%m-%d") if isinstance(created_at, datetime) else str(created_at)

        embed.set_footer(text=CONST.STRINGS["rooster_created_at"].format(created_at_str))

        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="newrooster",
        aliases=["createrooster", "createcock"],
    )
    @commands.guild_only()
    async def newrooster(
        self,
        ctx: commands.Context[Luminara],
        name: str,
    ) -> None:
        """
        Create a new rooster.

        Parameters
        ----------
        ctx : commands.Context[Luminara]
            The context of the command.
        name : str
            The name for your new rooster.
        """
        rooster_service = RoosterService(ctx.author.id)

        if rooster_service.has_rooster():
            if rooster_service.rooster is None:
                # This should not happen since has_rooster() would be False
                return

            embed = Builder.create_embed(
                Builder.ERROR,
                user_name=ctx.author.name,
                author_text=CONST.STRINGS["rooster_already_exists_author"],
                description=CONST.STRINGS["rooster_already_exists"].format(rooster_service.rooster["name"]),
            )
            await ctx.send(embed=embed)
            return

        rooster = rooster_service.create_rooster(name)
        if rooster is None:
            # This should not happen since we're creating a new rooster
            return

        embed = Builder.create_embed(
            Builder.SUCCESS,
            user_name=ctx.author.name,
            author_text=CONST.STRINGS["rooster_created_success_author"],
            description=CONST.STRINGS["rooster_created_success"].format(rooster["name"]),
        )

        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="train",
        aliases=["trainrooster"],
    )
    @commands.guild_only()
    async def train(
        self,
        ctx: commands.Context[Luminara],
        attribute: str,
    ) -> None:
        """
        Train your rooster to improve an attribute.

        Parameters
        ----------
        ctx : commands.Context[Luminara]
            The context of the command.
        attribute : str
            The attribute to train (strength, agility, endurance, technique, luck).
        """
        valid_attributes = ["strength", "agility", "endurance", "technique", "luck"]
        attribute = attribute.lower()

        if attribute not in valid_attributes:
            msg = f"Invalid attribute. Must be one of: {', '.join(valid_attributes)}"
            raise LumiException(msg)

        rooster_service = RoosterService(ctx.author.id)

        if not rooster_service.has_rooster():
            embed = Builder.create_embed(
                Builder.ERROR,
                user_name=ctx.author.name,
                author_text=CONST.STRINGS["rooster_no_rooster_author"],
                description=CONST.STRINGS["rooster_no_rooster"],
            )
            await ctx.send(embed=embed)
            return

        rooster = rooster_service.train_rooster(attribute)
        if rooster is None:
            # This should not happen since we checked has_rooster() above
            return

        embed = Builder.create_embed(
            Builder.SUCCESS,
            user_name=ctx.author.name,
            author_text=CONST.STRINGS["rooster_trained_success_author"],
            description=CONST.STRINGS["rooster_trained_success"].format(rooster["name"], attribute),
        )

        await ctx.send(embed=embed)


async def setup(bot: Luminara) -> None:
    await bot.add_cog(Rooster(bot))
