import json


def load_strings(path="config/strings.en-US.json"):
    with open(path, 'r') as file:
        data = json.load(file)

    return data
