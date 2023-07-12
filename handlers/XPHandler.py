import logging
import time

from data.Currency import Currency
from data.Xp import Xp
from sb_tools import level_messages

racu_logs = logging.getLogger('Racu.Core')


class XPHandler:
    def __init__(self):
        pass

    async def process_xp(self, message):

        if message.channel.id == 746796138195058788:
            racu_logs.info(f"No XP gain - spam channel. | user {message.author.name}")
            return

        current_time = time.time()
        user_id = message.author.id
        xp = Xp(user_id)

        if xp.ctime and current_time < xp.ctime:
            racu_logs.debug(f"XP UPDATE --- {message.author.name} sent a message but is on XP cooldown.")
            return

        new_xp = xp.xp + xp.xp_gain
        xp_needed_for_new_level = Xp.xp_needed_for_next_level(xp.level)

        if new_xp >= xp_needed_for_new_level:
            xp.level += 1
            xp.xp = 0

            await message.channel.send(content=f"<@{user_id}> {level_messages.load_level_message(xp.level)}")

            if xp.level in [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]:
                await self.assign_level_role(message.author, xp.level)

            """
            AWARD CURRENY_SPECIAL ON LEVEL-UP
            """
            user_currency = Currency(user_id)
            user_currency.add_special(1)
            user_currency.push()

            racu_logs.info(f"XP UPDATE --- {message.author.name} leveled up; new_level = {xp.level}.")

        else:
            xp.xp += xp.xp_gain
            racu_logs.info(f"XP UPDATE --- {message.author.name} gained {xp.xp_gain} XP; new_xp = {new_xp}.")

        xp.ctime = current_time + xp.new_cooldown
        xp.push()

        """
        Level calculation
        Linear = 9x + 27
        """

    @staticmethod
    async def assign_level_role(user, level):
        level_roles = {
            "level_5": 1118491431036792922,
            "level_10": 1118491486259003403,
            "level_15": 1118491512536301570,
            "level_20": 1118491532111126578,
            "level_25": 1118491554005393458,
            "level_30": 1118491572770713710,
            "level_35": 1118491596820840492,
            "level_40": 1118491622045405287,
            "level_45": 1118491650721853500,
            "level_50": 1118491681004732466,
            # Add more level roles as needed
        }

        guild = user.guild

        if guild.id != 719227135151046699:
            return

        current_level_role = None
        new_level_role_id = level_roles.get(f"level_{level}")

        for role in user.roles:
            if role.id in level_roles.values() and role.id != new_level_role_id:
                current_level_role = role
                break

        new_level_role = guild.get_role(new_level_role_id)
        await user.add_roles(new_level_role)

        if current_level_role:
            await user.remove_roles(current_level_role)
