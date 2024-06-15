import json
import logging

logs = logging.getLogger('Lumi.Core')


class JsonCache:
    _cache = {}

    @staticmethod
    def read_json(path):
        """Read and cache the JSON data if not already cached."""
        if path not in JsonCache._cache:
            with open(f"config/JSON/{path}.json", 'r') as file:
                JsonCache._cache[path] = json.load(file)
                logs.info(f"[JsonParser] {path}.json was loaded and cached.")

        return JsonCache._cache[path]
