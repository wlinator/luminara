import os
from typing import Optional, Set, List, Dict
import yaml
import json


class _parser:
    _yaml_cache = {}
    _json_cache = {}

    def read_yaml(self, path):
        if path not in _parser._cache:
            with open(f"settings/{path}.yaml") as file:
                _parser._cache[path] = yaml.safe_load(file)

        return _parser._yaml_cache[path]

    def read_json(self, path):
        if path not in _parser._cache:
            with open(f"settings/responses/{path}.json") as file:
                _parser._cache[path] = json.load(file)

        return _parser._json_cache[path]


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
    SLOTS_MULTIPLIERS: Dict[str, float] = _settings["economy"]["slots_multipliers"]

    # art from git repository
    _fetch_url: str = _settings["fetch_url"]

    LOGO_OPAQUE: str = _fetch_url + _settings["logo"]["opaque"]
    LOGO_TRANSPARENT: str = _fetch_url + _settings["logo"]["transparent"]
    ICONS_BOOST: str = _fetch_url + _settings["icons"]["boost"]
    ICONS_CHECK: str = _fetch_url + _settings["icons"]["check"]
    ICONS_CROSS: str = _fetch_url + _settings["icons"]["cross"]
    ICONS_EXCLAIM: str = _fetch_url + _settings["icons"]["exclaim"]
    ICONS_HAMMER: str = _fetch_url + _settings["icons"]["hammer"]
    ICONS_MONEY_BAG: str = _fetch_url + _settings["icons"]["money_bag"]
    ICONS_MONEY_COINS: str = _fetch_url + _settings["icons"]["money_coins"]
    ICONS_QUESTION: str = _fetch_url + _settings["icons"]["question"]
    ICONS_STREAK: str = _fetch_url + _settings["icons"]["streak"]
    ICONS_STREAK_BRONZE: str = _fetch_url + _settings["icons"]["streak_bronze"]
    ICONS_STREAK_GOLD: str = _fetch_url + _settings["icons"]["streak_gold"]
    ICONS_STREAK_SILVER: str = _fetch_url + _settings["icons"]["streak_silver"]
    ICONS_WARNING: str = _fetch_url + _settings["icons"]["warning"]
    JUICYBBLUE_FLOWERS: str = _fetch_url + _settings["juicybblue"]["flowers"]
    JUICYBBLUE_TEAPOT: str = _fetch_url + _settings["juicybblue"]["teapot"]
    JUICYBBLUE_MUFFIN: str = _fetch_url + _settings["juicybblue"]["muffin"]

    # art from imgur
    IMGUR_CLOUD: str = _settings["other"]["cloud"]
    IMGUR_TROPHY: str = _settings["other"]["trophy"]

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
    STRINGS = _parser().read_json("responses/strings.en-US")
    LEVEL_MESSAGES = _parser().read_json("responses/levels.en-US")

    # birthday messages
    _bday = _parser().read_json("responses/bdays.en-US")
    BIRTHDAY_MESSAGES = _bday["birthday_messages"]
    BIRTHDAY_MONTHS = _bday["months"]


CONST = Constants()
