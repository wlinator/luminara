import json
import yaml
from loguru import logger


class JsonCache:
    _cache = {}

    @staticmethod
    def read_json(path):
        """Read and cache the JSON data if not already cached."""
        if path not in JsonCache._cache:
            with open(f"config/JSON/{path}.json", "r") as file:
                JsonCache._cache[path] = json.load(file)
                logger.debug(f"{path}.json was loaded and cached.")

        return JsonCache._cache[path]


class YamlCache:
    _cache = {}

    @staticmethod
    def read_credentialsl():
        """Read and cache the creds.yaml data if not already cached."""
        path = "creds"
        if path not in YamlCache._cache:
            with open(f"{path}.yaml", "r") as file:
                YamlCache._cache[path] = yaml.safe_load(file)
                logger.debug(f"{path}.yaml was loaded and cached.")

        return YamlCache._cache[path]
