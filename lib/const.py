import json
import os
from collections.abc import Callable
from pathlib import Path
from typing import Any, Final

import yaml


class Parser:
    """Internal parses class. Not intended to be used outside of this module."""

    def __init__(self):
        self._cache: dict[str, Any] = {}

    def read_s(self) -> dict[str, Any]:
        if "settings" not in self._cache:
            self._cache["settings"] = self._read_file("settings.yaml", yaml.safe_load)
        return self._cache["settings"]

    def read_json(self, path: str) -> dict[str, Any]:
        cache_key = f"json_{path}"
        if cache_key not in self._cache:
            self._cache[cache_key] = self._read_file(f"locales/{path}.json", json.load)
        return self._cache[cache_key]

    def _read_file(self, file_path: str, load_func: Callable[[Any], dict[str, Any]]) -> dict[str, Any]:
        with Path(file_path).open() as file:
            return load_func(file)


class Constants:
    _p: Final = Parser()
    _s: Final = Parser().read_s()

    # bot credentials
    TOKEN: Final[str | None] = os.environ.get("TOKEN")
    INSTANCE: Final[str | None] = os.environ.get("INSTANCE")
    OWNER_IDS: Final[set[int]] = {int(oid) for oid in os.environ.get("OWNER_IDS", "").split(",") if oid.strip()}
    XP_GAIN_PER_MESSAGE: Final[int] = int(os.environ.get("XP_GAIN_PER_MESSAGE", 1))
    XP_GAIN_COOLDOWN: Final[int] = int(os.environ.get("XP_GAIN_COOLDOWN", 8))
    DBX_TOKEN: Final[str | None] = os.environ.get("DBX_OAUTH2_REFRESH_TOKEN")
    DBX_APP_KEY: Final[str | None] = os.environ.get("DBX_APP_KEY")
    DBX_APP_SECRET: Final[str | None] = os.environ.get("DBX_APP_SECRET")
    MARIADB_USER: Final[str | None] = os.environ.get("MARIADB_USER")
    MARIADB_PASSWORD: Final[str | None] = os.environ.get("MARIADB_PASSWORD")
    MARIADB_ROOT_PASSWORD: Final[str | None] = os.environ.get("MARIADB_ROOT_PASSWORD")
    MARIADB_DATABASE: Final[str | None] = os.environ.get("MARIADB_DATABASE")

    # twitch credentials
    TWITCH_CLIENT_ID: Final[str | None] = os.environ.get("TWITCH_CLIENT_ID")
    TWITCH_CLIENT_SECRET: Final[str | None] = os.environ.get("TWITCH_CLIENT_SECRET")

    # metadata
    TITLE: Final[str] = _s["info"]["title"]
    AUTHOR: Final[str] = _s["info"]["author"]
    LICENSE: Final[str] = _s["info"]["license"]
    VERSION: Final[str] = _s["info"]["version"]
    REPO_URL: Final[str] = _s["info"]["repository_url"]
    INVITE_URL: Final[str] = _s["info"]["invite_url"]

    # loguru
    LOG_LEVEL: Final[str] = _s["logs"]["level"] or "DEBUG"
    LOG_FORMAT: Final[str] = _s["logs"]["format"]

    # cogs
    COG_IGNORE_LIST: Final[set[str]] = set(_s["cogs"]["ignore"]) if _s["cogs"]["ignore"] else set()

    # images
    ALLOWED_IMAGE_EXTENSIONS: Final[list[str]] = _s["images"]["allowed_image_extensions"]
    BIRTHDAY_GIF_URL: Final[str] = _s["images"]["birthday_gif_url"]

    # colors
    COLOR_DEFAULT: Final[int] = _s["colors"]["color_default"]
    COLOR_WARNING: Final[int] = _s["colors"]["color_warning"]
    COLOR_ERROR: Final[int] = _s["colors"]["color_error"]

    # economy
    DAILY_REWARD: Final[int] = _s["economy"]["daily_reward"]
    BLACKJACK_MULTIPLIER: Final[float] = _s["economy"]["blackjack_multiplier"]
    BLACKJACK_HIT_EMOJI: Final[str] = _s["economy"]["blackjack_hit_emoji"]
    BLACKJACK_STAND_EMOJI: Final[str] = _s["economy"]["blackjack_stand_emoji"]
    SLOTS_MULTIPLIERS: Final[dict[str, float]] = _s["economy"]["slots_multipliers"]

    # art from git repository
    _fetch_url: Final[str] = _s["art"]["fetch_url"]

    LUMI_LOGO_OPAQUE: Final[str] = _fetch_url + _s["art"]["logo"]["opaque"]
    LUMI_LOGO_TRANSPARENT: Final[str] = _fetch_url + _s["art"]["logo"]["transparent"]
    BOOST_ICON: Final[str] = _fetch_url + _s["art"]["icons"]["boost"]
    CHECK_ICON: Final[str] = _fetch_url + _s["art"]["icons"]["check"]
    CROSS_ICON: Final[str] = _fetch_url + _s["art"]["icons"]["cross"]
    EXCLAIM_ICON: Final[str] = _fetch_url + _s["art"]["icons"]["exclaim"]
    INFO_ICON: Final[str] = _fetch_url + _s["art"]["icons"]["info"]
    HAMMER_ICON: Final[str] = _fetch_url + _s["art"]["icons"]["hammer"]
    MONEY_BAG_ICON: Final[str] = _fetch_url + _s["art"]["icons"]["money_bag"]
    MONEY_COINS_ICON: Final[str] = _fetch_url + _s["art"]["icons"]["money_coins"]
    QUESTION_ICON: Final[str] = _fetch_url + _s["art"]["icons"]["question"]
    STREAK_ICON: Final[str] = _fetch_url + _s["art"]["icons"]["streak"]
    STREAK_BRONZE_ICON: Final[str] = _fetch_url + _s["art"]["icons"]["streak_bronze"]
    STREAK_GOLD_ICON: Final[str] = _fetch_url + _s["art"]["icons"]["streak_gold"]
    STREAK_SILVER_ICON: Final[str] = _fetch_url + _s["art"]["icons"]["streak_silver"]
    WARNING_ICON: Final[str] = _fetch_url + _s["art"]["icons"]["warning"]

    # art from imgur
    FLOWERS_ART: Final[str] = _s["art"]["juicybblue"]["flowers"]
    TEAPOT_ART: Final[str] = _s["art"]["juicybblue"]["teapot"]
    MUFFIN_ART: Final[str] = _s["art"]["juicybblue"]["muffin"]
    CLOUD_ART: Final[str] = _s["art"]["other"]["cloud"]
    TROPHY_ART: Final[str] = _s["art"]["other"]["trophy"]

    # emotes
    EMOTES_SERVER_ID: Final[int] = _s["emotes"]["guild_id"]
    EMOTE_IDS: Final[dict[str, int]] = _s["emotes"]["emote_ids"]

    # introductions (currently only usable in ONE guild)
    INTRODUCTIONS_GUILD_ID: Final[int] = _s["introductions"]["intro_guild_id"]
    INTRODUCTIONS_CHANNEL_ID: Final[int] = _s["introductions"]["intro_channel_id"]
    INTRODUCTIONS_QUESTION_MAPPING: Final[dict[str, str]] = _s["introductions"]["intro_question_mapping"]

    # Reponse strings
    # TODO: Implement switching between languages
    STRINGS: Final = _p.read_json("strings.en-US")
    LEVEL_MESSAGES: Final = _p.read_json("levels.en-US")

    _bday: Final = _p.read_json("bdays.en-US")
    BIRTHDAY_MESSAGES: Final[list[str]] = _bday["birthday_messages"]
    BIRTHDAY_MONTHS: Final[list[str]] = _bday["months"]

    # XP config at bot admin level
    XP_EXCLUDED_CHANNEL_IDS: Final[list[int]] = _s["xp"]["excluded_channel_ids"]


CONST = Constants()
