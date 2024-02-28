import json
import logging

logs = logging.getLogger('Racu.Core')


def load_strings(path="config/strings.en-US.json"):
    with open(path, 'r') as file:
        data = json.load(file)

    logs.debug(f"{path} was loaded.")
    return data


def load_levels(path="config/levels.en-US.json"):
    with open(path, 'r') as file:
        data = json.load(file)

    logs.debug(f"{path} was loaded.")
    return data


def load_economy_config(path="config/economy.json"):
    with open(path, 'r') as file:
        data = json.load(file)

    logs.debug(f"{path} was loaded.")
    return data


def load_reactions(path="config/reactions.json"):
    with open(path, 'r') as file:
        data = json.load(file)

    logs.debug(f"{path} was loaded.")
    return data


def load_birthday_messages(path="config/birthday.json"):
    with open(path, 'r') as file:
        data = json.load(file)

    logs.debug(f"{path} was loaded.")
    return data
