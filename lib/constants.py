import os
from typing import Optional, Set

from config.parser import JsonCache


class Constants:
    # JSON raw
    ART = JsonCache.read_json("art")
    RESOURCES = JsonCache.read_json("resources")
    LEVEL_MESSAGES = JsonCache.read_json("levels")

    # metadata
    TITLE = "Luminara"
    AUTHOR = "wlinator"
    LICENSE = "GNU General Public License v3.0"
    VERSION = "2.8.12"  # "Refactor Blackjack" update

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

    # config
    ALLOWED_IMAGE_EXTENSIONS = (".jpg", ".png")

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
    KRC_QUESTION_MAPPING: dict[str, str] = RESOURCES["guild_specific"][
        "question_mapping"
    ]

    # logo
    LUMI_LOGO_TRANSPARENT = ART["logo"]["transparent"]
    LUMI_LOGO_OPAQUE = ART["logo"]["opaque"]

    # icons art
    BOOST_ICON = ART["icons"]["boost"]
    CHECK_ICON = ART["icons"]["check"]
    CROSS_ICON = ART["icons"]["cross"]
    EXCLAIM_ICON = ART["icons"]["exclaim"]
    HAMMER_ICON = ART["icons"]["hammer"]
    MONEY_BAG_ICON = ART["icons"]["money_bag"]
    MONEY_COINS_ICON = ART["icons"]["money_coins"]
    QUESTION_ICON = ART["icons"]["question"]
    STREAK_ICON = ART["icons"]["streak"]
    WARNING_ICON = ART["icons"]["warning"]

    # art by JuicyBblue
    FLOWERS_ART = ART["juicybblue"]["flowers"]
    TEAPOT_ART = ART["juicybblue"]["teapot"]
    MUFFIN_ART = ART["juicybblue"]["muffin"]

    # other art
    CLOUD_ART = ART["other"]["cloud"]
    TROPHY_ART = ART["other"]["trophy"]

    # birthdays
    BIRTHDAY_MESSAGES = JsonCache.read_json("birthday")["birthday_messages"]
    BIRTHDAY_MONTHS = JsonCache.read_json("birthday")["months"]
    BIRTHDAY_GIF_URL = "https://media1.tenor.com/m/NXvU9jbBUGMAAAAC/fireworks.gif"

    # economy
    DAILY_REWARD = RESOURCES["daily_reward"]
    SLOTS = RESOURCES["slots"]
    BLACKJACK = RESOURCES["blackjack"]


CONST = Constants()
