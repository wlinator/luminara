import json

from db import database


class BlackJackStats:
    def __init__(self, user_id, is_won, bet, payout, hand_player, hand_dealer):
        self.user_id = user_id
        self.is_won = is_won
        self.bet = bet
        self.payout = payout
        self.hand_player = json.dumps(hand_player)
        self.hand_dealer = json.dumps(hand_dealer)

    def push(self):
        query = """
        INSERT INTO stats_bj (user_id, is_won, bet, payout, hand_player, hand_dealer)
        VALUES (?, ?, ?, ?, ?, ?)
        """

        values = (self.user_id, self.is_won, self.bet, self.payout, self.hand_player, self.hand_dealer)

        database.execute_query(query, values)

    @staticmethod
    def fetch_all():
        query = "SELECT * FROM stats_bj"
        rows = database.select_query(query)

        stats_list = []
        for row in rows:
            # extract individual columns from the row
            id, user_id, is_won, bet, payout, hand_player_json, hand_dealer_json = row

            # convert hands from JSON strings to lists
            hand_player = json.loads(hand_player_json)
            hand_dealer = json.loads(hand_dealer_json)

            # assign to dictionary
            stats_data = {
                'id': id,
                'user_id': user_id,
                'is_won': bool(is_won),
                'bet': bet,
                'payout': payout,
                'hand_player': hand_player,
                'hand_dealer': hand_dealer
            }

            # add the row to the list
            stats_list.append(stats_data)

        return stats_list
