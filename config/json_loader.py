import json
import logging

racu_logs = logging.getLogger('Racu.Core')


def load_strings(path="config/strings.en-US.json"):
    with open(path, 'r') as file:
        data = json.load(file)

    racu_logs.debug(f"{path} was loaded.")
    return data


def load_levels(path="config/levels.en-US.json"):
    with open(path, 'r') as file:
        data = json.load(file)

    racu_logs.debug(f"{path} was loaded.")
    return data


def load_economy_config(path="config/economy.json"):
    with open(path, 'r') as file:
        data = json.load(file)

    racu_logs.debug(f"{path} was loaded.")
    return data


def load_reactions(path="config/reactions.json"):
    with open(path, 'r') as file:
        data = json.load(file)

    racu_logs.debug(f"{path} was loaded.")
    return data
