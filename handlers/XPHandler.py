import logging
import random
import time

from config import json_loader
from services.Currency import Currency
from services.Xp import Xp

logs = logging.getLogger('Racu.Core')
strings = json_loader.load_strings()
level_messages = json_loader.load_levels()


def level_message(level, author):
    if level in [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]:
        return strings["level_up_reward"].format(author.name, level)
    else:
        return strings["level_up"].format(author.name, level)


def level_messages_v2(level, author):
    """
    v2 of the level messages, randomized output from JSON.
    Checks if the level is within a bracket -> generic fallback
    :param level:
    :param author:
    :return:
    """

    # checks if level is a multiple of 5 within the range of 5 to 100 (inclusive)
    if level % 5 == 0 and 5 <= level <= 100:
        return strings["level_up_reward"].format(author.name, level)

    level_range = None
    for key in level_messages.keys():
        start, end = map(int, key.split('-'))
        if start <= level <= end:
            level_range = key
            break

    if level_range is None:
        # not in range of JSON
        return strings["level_up"].format(author.name, level)

    message_list = level_messages[level_range]
    random_message = random.choice(message_list)
    start_string = strings["level_up_prefix"].format(author.name)
    return start_string + random_message.format(level)


class XPHandler:
    def __init__(self):
        pass

    async def process_xp(self, message):

        if message.channel.id == 746796138195058788 or message.channel.id == 814590778650263604:
            logs.info(f"[XpHandler] {message.author.name} sent a message in a xp-blacklisted channel.")
            return

        current_time = time.time()
        user_id = message.author.id
        xp = Xp(user_id)

        if xp.ctime and current_time < xp.ctime:
            logs.info(f"[XpHandler] {message.author.name} sent a message but is on XP cooldown.")
            return

        new_xp = xp.xp + xp.xp_gain
        xp_needed_for_new_level = Xp.xp_needed_for_next_level(xp.level)

        if new_xp >= xp_needed_for_new_level:
            xp.level += 1
            xp.xp = 0

            try:
                lvl_message = level_messages_v2(xp.level, message.author)
            except Exception as err:
                # fallback to v1 (generic leveling)
                lvl_message = level_messages(xp.level, message.author)
                logs.error("[XpHandler] level_messages v1 fallback was triggered: ", err)

            await message.reply(content=lvl_message)
            
            # checks if xp.level is a multiple of 5 within the range of 5 to 100 (inclusive)
            if xp.level % 5 == 0 and 5 <= xp.level <= 100:
                try:
                    await self.assign_level_role(message.author, xp.level)
                except Exception as error:
                    logs.error(f"[XpHandler] Assign level role FAILED; {error}")

            """
            AWARD CURRENY_SPECIAL ON LEVEL-UP
            """
            user_currency = Currency(user_id)
            user_currency.add_special(1)
            user_currency.push()

            logs.info(f"[XpHandler] {message.author.name} leveled up to lv {xp.level}.")

        else:
            xp.xp += xp.xp_gain
            logs.info(f"[XpHandler] {message.author.name} gained {xp.xp_gain} XP | "
                           f"lv {xp.level} with {xp.xp} XP.")

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
            "level_55": 1191681166848303135,
            "level_60": 1191681220145319956,
            "level_65": 1191681253322264587,
            "level_70": 1191681274180554792,
            "level_75": 1191681293277216859,
            "level_80": 1191681312269017180,
            "level_85": 1191681337560662086,
            "level_90": 1191681359995998209,
            "level_95": 1191681384113262683,
            "level_100": 1191681405445492778,
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
