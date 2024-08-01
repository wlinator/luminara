import os
from typing import Optional, Set

from config.parser import JsonCache

art = JsonCache.read_json("art")
resources = JsonCache.read_json("resources")


class Constants:
    # metadata
    TITLE = "Luminara"
    AUTHOR = "wlinator"
    LICENSE = "GNU General Public License v3.0"
    VERSION = "2.7.0"

    # bot credentials
    TOKEN: Optional[str] = os.environ.get("TOKEN", None)
    INSTANCE: Optional[str] = os.environ.get("INSTANCE", None)

    OWNER_IDS: Optional[Set[int]] = (
        {int(id.strip()) for id in os.environ.get("OWNER_ID", "").split(",") if id}
        if os.environ.get("OWNER_ID")
        else None
    )

    XP_GAIN_PER_MESSAGE: int = int(os.environ.get("XP_GAIN_PER_MESSAGE", 1))
    XP_GAIN_COOLDOWN: int = int(os.environ.get("XP_GAIN_COOLDOWN", 8))

    DBX_TOKEN: Optional[str] = os.environ.get("DBX_OAUTH2_REFRESH_TOKEN", None)
    DBX_APP_KEY: Optional[str] = os.environ.get("DBX_APP_KEY", None)
    DBX_APP_SECRET: Optional[str] = os.environ.get("DBX_APP_SECRET", None)

    MARIADB_USER: Optional[str] = os.environ.get("MARIADB_USER", None)
    MARIADB_PASSWORD: Optional[str] = os.environ.get("MARIADB_PASSWORD", None)
    MARIADB_ROOT_PASSWORD: Optional[str] = os.environ.get("MARIADB_ROOT_PASSWORD", None)
    MARIADB_DATABASE: Optional[str] = os.environ.get("MARIADB_DATABASE", None)

    # emotes
    EMOTES_GUILD_ID = 1038051105642401812

    # color scheme
    COLOR_DEFAULT = 0xFF8C00
    COLOR_WARNING = 0xFF7600
    COLOR_ERROR = 0xFF4500

    # strings
    STRINGS = JsonCache.read_json("strings")

    # repository
    REPO_URL = "https://git.wlinator.org/Luminara/Lumi"
    INVITE_LINK = "https://discord.com/oauth2/authorize?client_id=1038050427272429588&permissions=8&scope=bot"

    # KRC
    KRC_GUILD_ID: int = 719227135151046699
    KRC_INTRO_CHANNEL_ID: int = 973619250507972618
    KRC_QUESTION_MAPPING: dict[str, str] = resources["guild_specific"][
        "question_mapping"
    ]

    # logo
    LUMI_LOGO_TRANSPARENT = art["logo"]["transparent"]
    LUMI_LOGO_OPAQUE = art["logo"]["opaque"]

    # icons art
    BOOST_ICON = art["icons"]["boost"]
    CHECK_ICON = art["icons"]["check"]
    CROSS_ICON = art["icons"]["cross"]
    EXCLAIM_ICON = art["icons"]["exclaim"]
    HAMMER_ICON = art["icons"]["hammer"]
    MONEY_BAG_ICON = art["icons"]["money_bag"]
    MONEY_COINS_ICON = art["icons"]["money_coins"]
    QUESTION_ICON = art["icons"]["question"]
    STREAK_ICON = art["icons"]["streak"]
    WARNING_ICON = art["icons"]["warning"]

    # art by JuicyBblue
    FLOWERS_ART = art["juicybblue"]["flowers"]
    TEAPOT_ART = art["juicybblue"]["teapot"]
    MUFFIN_ART = art["juicybblue"]["muffin"]

    # birthdays
    BIRTHDAY_MESSAGES = JsonCache.read_json("birthday")["birthday_messages"]
    BIRTHDAY_MONTHS = JsonCache.read_json("birthday")["months"]


CONST = Constants()


CONST = Constants()
