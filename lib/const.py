import os
import json
import yaml
from functools import lru_cache
from typing import Optional, Callable, Set


class _parser:
    """Internal parses class. Not intended to be used outside of this module."""

    @lru_cache(maxsize=1024)
    def read_settings(self) -> dict:
        return self._read_file("settings.yaml", yaml.safe_load)

    def read_json(self, path: str) -> dict:
        return self._read_file(f"localization/{path}.json", json.load)

    def _read_file(self, file_path: str, load_func: Callable) -> dict:
        with open(file_path) as file:
            return load_func(file)


class _constants:
    _p = _parser()
    _s = _parser().read_settings()

    # bot credentials
    TOKEN: Optional[str] = os.getenv("TOKEN")

    OWNER_IDS: Optional[Set[int]] = (
        {int(id.strip()) for id in os.environ.get("OWNER_IDS", "").split(",") if id}
        if "OWNER_IDS" in os.environ
        else None
    )

    # settings
    LOG_LEVEL: str = _s["logs"]["level"] or "DEBUG"
    LOG_FORMAT: str = _s["logs"]["format"]
    COG_IGNORE_LIST: Set[str] = (
        set(_s["cogs"]["ignore"]) if _s["cogs"]["ignore"] else set()
    )

    # Reponse strings
    # TODO: Implement switching between languages
    STRINGS = _p.read_json("strings.en-US")
    LEVEL_MESSAGES = _p.read_json("levels.en-US")

    _bday = _p.read_json("bdays.en-US")
    BIRTHDAY_MESSAGES = _bday["birthday_messages"]
    BIRTHDAY_MONTHS = _bday["months"]


CONST: _constants = _constants()
