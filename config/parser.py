import json


class JsonCache:
    _cache = {}

    @staticmethod
    def read_json(path):
        """Read and cache the JSON data if not already cached."""
        if path not in JsonCache._cache:
            with open(f"config/JSON/{path}.json") as file:
                JsonCache._cache[path] = json.load(file)

        return JsonCache._cache[path]
