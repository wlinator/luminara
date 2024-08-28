import os
import json
import yaml
from functools import lru_cache
from typing import Optional, Callable, Set, List, Dict


class _parser:
    """Internal parses class. Not intended to be used outside of this module."""

    @lru_cache(maxsize=1024)
    def read_s(self) -> dict:
        return self._read_file("settings.yaml", yaml.safe_load)

    def read_json(self, path: str) -> dict:
        return self._read_file(f"localization/{path}.json", json.load)

    def _read_file(self, file_path: str, load_func: Callable) -> dict:
        with open(file_path) as file:
            return load_func(file)


class _constants:
    _p = _parser()
    _s = _parser().read_s()

    # bot credentials
    TOKEN: Optional[str] = os.environ.get("TOKEN")
    INSTANCE: Optional[str] = os.environ.get("INSTANCE")
    XP_GAIN_PER_MESSAGE: int = int(os.environ.get("XP_GAIN_PER_MESSAGE", 1))
    XP_GAIN_COOLDOWN: int = int(os.environ.get("XP_GAIN_COOLDOWN", 8))
    DBX_TOKEN: Optional[str] = os.environ.get("DBX_OAUTH2_REFRESH_TOKEN")
    DBX_APP_KEY: Optional[str] = os.environ.get("DBX_APP_KEY")
    DBX_APP_SECRET: Optional[str] = os.environ.get("DBX_APP_SECRET")
    MARIADB_USER: Optional[str] = os.environ.get("MARIADB_USER")
    MARIADB_PASSWORD: Optional[str] = os.environ.get("MARIADB_PASSWORD")
    MARIADB_ROOT_PASSWORD: Optional[str] = os.environ.get("MARIADB_ROOT_PASSWORD")
    MARIADB_DATABASE: Optional[str] = os.environ.get("MARIADB_DATABASE")

    OWNER_IDS: Optional[Set[int]] = (
        {int(id.strip()) for id in os.environ.get("OWNER_IDS", "").split(",") if id}
        if "OWNER_IDS" in os.environ
        else None
    )

    # metadata
    TITLE: str = _s["info"]["title"]
    AUTHOR: str = _s["info"]["author"]
    LICENSE: str = _s["info"]["license"]
    VERSION: str = _s["info"]["version"]
    REPO_URL: str = _s["info"]["repository_url"]
    INVITE_URL: str = _s["info"]["invite_url"]

    # loguru
    LOG_LEVEL: str = _s["logs"]["level"] or "DEBUG"
    LOG_FORMAT: str = _s["logs"]["format"]

    # cogs
    COG_IGNORE_LIST: Set[str] = (
        set(_s["cogs"]["ignore"]) if _s["cogs"]["ignore"] else set()
    )

    # images
    ALLOWED_IMAGE_EXTENSIONS: List[str] = _s["images"]["allowed_image_extensions"]
    BIRTHDAY_GIF_URL: str = _s["images"]["birthday_gif_url"]

    # colors
    COLOR_DEFAULT: int = _s["colors"]["color_default"]
    COLOR_WARNING: int = _s["colors"]["color_warning"]
    COLOR_ERROR: int = _s["colors"]["color_error"]

    # economy
    DAILY_REWARD: int = _s["economy"]["daily_reward"]
    BLACKJACK_MULTIPLIER: float = _s["economy"]["blackjack_multiplier"]
    BLACKJACK_HIT_EMOJI: str = _s["economy"]["blackjack_hit_emoji"]
    BLACKJACK_STAND_EMOJI: str = _s["economy"]["blackjack_stand_emoji"]
    SLOTS_MULTIPLIERS: Dict[str, float] = _s["economy"]["slots_multipliers"]

    # art from git repository
    _fetch_url: str = _s["art"]["fetch_url"]

    LUMI_LOGO_OPAQUE: str = _fetch_url + _s["art"]["logo"]["opaque"]
    LUMI_LOGO_TRANSPARENT: str = _fetch_url + _s["art"]["logo"]["transparent"]
    BOOST_ICON: str = _fetch_url + _s["art"]["icons"]["boost"]
    CHECK_ICON: str = _fetch_url + _s["art"]["icons"]["check"]
    CROSS_ICON: str = _fetch_url + _s["art"]["icons"]["cross"]
    EXCLAIM_ICON: str = _fetch_url + _s["art"]["icons"]["exclaim"]
    HAMMER_ICON: str = _fetch_url + _s["art"]["icons"]["hammer"]
    MONEY_BAG_ICON: str = _fetch_url + _s["art"]["icons"]["money_bag"]
    MONEY_COINS_ICON: str = _fetch_url + _s["art"]["icons"]["money_coins"]
    QUESTION_ICON: str = _fetch_url + _s["art"]["icons"]["question"]
    STREAK_ICON: str = _fetch_url + _s["art"]["icons"]["streak"]
    STREAK_BRONZE_ICON: str = _fetch_url + _s["art"]["icons"]["streak_bronze"]
    STREAK_GOLD_ICON: str = _fetch_url + _s["art"]["icons"]["streak_gold"]
    STREAK_SILVER_ICON: str = _fetch_url + _s["art"]["icons"]["streak_silver"]
    WARNING_ICON: str = _fetch_url + _s["art"]["icons"]["warning"]

    # art from imgur
    FLOWERS_ART: str = _s["art"]["juicybblue"]["flowers"]
    TEAPOT_ART: str = _s["art"]["juicybblue"]["teapot"]
    MUFFIN_ART: str = _s["art"]["juicybblue"]["muffin"]
    CLOUD_ART: str = _s["art"]["other"]["cloud"]
    TROPHY_ART: str = _s["art"]["other"]["trophy"]

    # emotes
    EMOTES_SERVER_ID: int = _s["emotes"]["guild_id"]
    EMOTE_IDS: Dict[str, int] = _s["emotes"]["emote_ids"]

    # introductions (currently only usable in ONE guild)
    INTRODUCTIONS_GUILD_ID: int = _s["introductions"]["intro_guild_id"]
    INTRODUCTIONS_CHANNEL_ID: int = _s["introductions"]["intro_channel_id"]
    INTRODUCTIONS_QUESTION_MAPPING: Dict[str, str] = _s["introductions"][
        "intro_question_mapping"
    ]

    # Reponse strings
    # TODO: Implement switching between languages
    STRINGS = _p.read_json("strings.en-US")
    LEVEL_MESSAGES = _p.read_json("levels.en-US")

    _bday = _p.read_json("bdays.en-US")
    BIRTHDAY_MESSAGES = _bday["birthday_messages"]
    BIRTHDAY_MONTHS = _bday["months"]


CONST: _constants = _constants()
