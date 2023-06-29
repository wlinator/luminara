import json


def load_strings(path="config/strings.en-US.json"):
    with open(path, 'r') as file:
        data = json.load(file)

    return data


def load_economy_config(path="config/economy.json"):
    with open(path, 'r') as file:
        data = json.load(file)

    return data


def load_reactions(path="config/reactions.json"):
    with open(path, 'r') as file:
        data = json.load(file)

    return data
