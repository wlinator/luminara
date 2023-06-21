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
    def count_games(user_id=None):
        if not user_id:
            # count ALL blackjack games
            query = "SELECT COUNT(*) FROM stats_bj"
            amount = database.select_query_one(query)
            return amount

    @staticmethod
    def get_investment_and_payout(user_id=None):
        if not user_id:
            # return from ALL blackjack games
            query = "SELECT SUM(bet), SUM(payout) FROM stats_bj"
            (investment, payout) = database.select_query(query)[0]
            return investment, payout

    @staticmethod
    def get_winning_and_losing_amount(user_id=None):
        if not user_id:
            # return from ALL blackjack games
            query = """
            SELECT
                SUM(CASE WHEN is_won = 1 THEN 1 ELSE 0 END) AS winning,
                SUM(CASE WHEN is_won = 0 THEN 1 ELSE 0 END) AS losing
            FROM stats_bj;
            """
            (winning, losing) = database.select_query(query)[0]
            return winning, losing

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
