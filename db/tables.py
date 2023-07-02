import logging

from db import database

racu_logs = logging.getLogger('Racu.Core')

xp_table = """
CREATE TABLE IF NOT EXISTS xp (
    user_id INTEGER PRIMARY KEY NOT NULL,
    user_xp INTEGER NOT NULL,
    user_level INTEGER NOT NULL,
    cooldown REAL
)
"""

currency_table = """
CREATE TABLE IF NOT EXISTS currency (
    user_id INTEGER PRIMARY KEY NOT NULL,
    cash_balance INTEGER NOT NULL,
    special_balance INTEGER
)
"""

item_table = """
CREATE TABLE IF NOT EXISTS item (
    id INTEGER PRIMARY KEY,
    name TEXT,
    display_name TEXT,
    description TEXT,
    image_url TEXT,
    emote_id INTEGER,
    quote TEXT,
    type TEXT
)
"""

inventory_table = """
CREATE TABLE IF NOT EXISTS inventory (
    user_id INTEGER,
    item_id INTEGER,
    quantity INTEGER,

    PRIMARY KEY (user_id, item_id),
    FOREIGN KEY (item_id) REFERENCES item (id)
)
"""

dailies_table = """
CREATE TABLE IF NOT EXISTS dailies (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    amount INTEGER,
    claimed_at REAL,
    streak INTEGER
)
"""

stats_bj = """
CREATE TABLE IF NOT EXISTS stats_bj (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    is_won INTEGER,
    bet INTEGER,
    payout INTEGER,
    hand_player TEXT,
    hand_dealer TEXT
)
"""

stats_slots = """
CREATE TABLE IF NOT EXISTS stats_slots (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    is_won INTEGER,
    bet INTEGER,
    payout INTEGER,
    spin_type TEXT,
    icons TEXT
)
"""

stats_duel = """
CREATE TABLE IF NOT EXISTS stats_duel (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    is_won INTEGER,
    bet INTEGER
)
"""


def sync_database():
    database.execute_query(xp_table)
    database.execute_query(currency_table)
    database.execute_query(item_table)
    database.execute_query(inventory_table)
    database.execute_query(dailies_table)
    database.execute_query(stats_bj)
    database.execute_query(stats_slots)
    database.execute_query(stats_duel)

    racu_logs.info("Database was synced.")
