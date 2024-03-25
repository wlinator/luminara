import json
import logging

logs = logging.getLogger('Racu.Core')


class JsonCache:
    _cache = {}

    @staticmethod
    def read_json(path):
        """Read and cache the JSON data if not already cached."""
        if path not in JsonCache._cache:
            with open(f"config/JSON/{path}.json", 'r') as file:
                JsonCache._cache[path] = json.load(file)
                logs.info(f"{path}.json was loaded and cached.")

        return JsonCache._cache[path]
