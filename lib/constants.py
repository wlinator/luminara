import os
from typing import Optional, Set, List, Dict
import yaml
import json
from functools import lru_cache


class _parser:
    """Internal parser class. Not intended for direct use outside this module."""

    @lru_cache(maxsize=1024)
    def read_yaml(self, path):
        return self._read_file(f"settings/{path}.yaml", yaml.safe_load)

    @lru_cache(maxsize=1024)
    def read_json(self, path):
        return self._read_file(f"settings/{path}.json", json.load)

    def _read_file(self, file_path, load_func):
        with open(file_path) as file:
            return load_func(file)


class Constants:
    _p = _parser()
    _settings = _p.read_yaml("settings")

    # bot credentials (.env file)
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
    TITLE: str = _settings["info"]["title"]
    AUTHOR: str = _settings["info"]["author"]
    LICENSE: str = _settings["info"]["license"]
    VERSION: str = _settings["info"]["version"]
    REPOSITORY_URL: str = _settings["info"]["repository_url"]

    # images
    ALLOWED_IMAGE_EXTENSIONS: List[str] = _settings["images"][
        "allowed_image_extensions"
    ]
    BIRTHDAY_GIF_URL: str = _settings["images"]["birthday_gif_url"]

    # colors
    COLOR_DEFAULT: int = _settings["colors"]["color_default"]
    COLOR_WARNING: int = _settings["colors"]["color_warning"]
    COLOR_ERROR: int = _settings["colors"]["color_error"]

    # economy
    DAILY_REWARD: int = _settings["economy"]["daily_reward"]
    BLACKJACK_MULTIPLIER: float = _settings["economy"]["blackjack_multiplier"]
    BLACKJACK_HIT_EMOJI: str = _settings["economy"]["blackjack_hit_emoji"]
    BLACKJACK_STAND_EMOJI: str = _settings["economy"]["blackjack_stand_emoji"]
    SLOTS_MULTIPLIERS: Dict[str, float] = _settings["economy"]["slots_multipliers"]

    # art from git repository
    _fetch_url: str = _settings["art"]["fetch_url"]

    LUMI_LOGO_OPAQUE: str = _fetch_url + _settings["art"]["logo"]["opaque"]
    LUMI_LOGO_TRANSPARENT: str = _fetch_url + _settings["art"]["logo"]["transparent"]
    BOOST_ICON: str = _fetch_url + _settings["art"]["icons"]["boost"]
    CHECK_ICON: str = _fetch_url + _settings["art"]["icons"]["check"]
    CROSS_ICON: str = _fetch_url + _settings["art"]["icons"]["cross"]
    EXCLAIM_ICON: str = _fetch_url + _settings["art"]["icons"]["exclaim"]
    HAMMER_ICON: str = _fetch_url + _settings["art"]["icons"]["hammer"]
    MONEY_BAG_ICON: str = _fetch_url + _settings["art"]["icons"]["money_bag"]
    MONEY_COINS_ICON: str = _fetch_url + _settings["art"]["icons"]["money_coins"]
    QUESTION_ICON: str = _fetch_url + _settings["art"]["icons"]["question"]
    STREAK_ICON: str = _fetch_url + _settings["art"]["icons"]["streak"]
    STREAK_BRONZE_ICON: str = _fetch_url + _settings["art"]["icons"]["streak_bronze"]
    STREAK_GOLD_ICON: str = _fetch_url + _settings["art"]["icons"]["streak_gold"]
    STREAK_SILVER_ICON: str = _fetch_url + _settings["art"]["icons"]["streak_silver"]
    WARNING_ICON: str = _fetch_url + _settings["art"]["icons"]["warning"]

    # art from imgur
    FLOWERS_ART: str = _settings["art"]["juicybblue"]["flowers"]
    TEAPOT_ART: str = _settings["art"]["juicybblue"]["teapot"]
    MUFFIN_ART: str = _settings["art"]["juicybblue"]["muffin"]
    CLOUD_ART: str = _settings["art"]["other"]["cloud"]
    TROPHY_ART: str = _settings["art"]["other"]["trophy"]

    # emotes
    EMOTES_SERVER_ID: int = _settings["emotes"]["guild_id"]
    EMOTE_IDS: Dict[str, int] = _settings["emotes"]["emote_ids"]

    # introductions (currently only usable in ONE guild)
    INTRODUCTIONS_GUILD_ID: int = _settings["introductions"]["intro_guild_id"]
    INTRODUCTIONS_CHANNEL_ID: int = _settings["introductions"]["intro_channel_id"]
    INTRODUCTIONS_QUESTION_MAPPING: Dict[str, str] = _settings["introductions"][
        "intro_question_mapping"
    ]

    # Response strings
    # TODO: Implement switching between languages
    STRINGS = _p.read_json("responses/strings.en-US")
    LEVEL_MESSAGES = _p.read_json("responses/levels.en-US")

    # birthday messages
    _bday = _p.read_json("responses/bdays.en-US")
    BIRTHDAY_MESSAGES = _bday["birthday_messages"]
    BIRTHDAY_MONTHS = _bday["months"]


CONST = Constants()
