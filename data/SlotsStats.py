import json

from db import database


class SlotsStats:
    def __init__(self, user_id, is_won, bet, payout, spin_type, icons):
        self.user_id = user_id
        self.is_won = is_won
        self.bet = bet
        self.payout = payout
        self.spin_type = spin_type
        self.icons = json.dumps(icons)

    def push(self):
        query = """
        INSERT INTO stats_slots (user_id, is_won, bet, payout, spin_type, icons)
        VALUES (?, ?, ?, ?, ?, ?)
        """

        values = (self.user_id, self.is_won, self.bet, self.payout, self.spin_type, self.icons)

        database.execute_query(query, values)
