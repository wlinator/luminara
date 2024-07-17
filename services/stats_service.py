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
        INSERT INTO blackjack (user_id, is_won, bet, payout, hand_player, hand_dealer)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            self.user_id,
            self.is_won,
            self.bet,
            self.payout,
            self.hand_player,
            self.hand_dealer,
        )

        database.execute_query(query, values)

    @staticmethod
    def get_user_stats(user_id):
        query = """
                SELECT
                    COUNT(*) AS amount_of_games,
                    SUM(bet) AS total_bet,
                    SUM(payout) AS total_payout,
                    SUM(CASE WHEN is_won = 1 THEN 1 ELSE 0 END) AS winning,
                    SUM(CASE WHEN is_won = 0 THEN 1 ELSE 0 END) AS losing
                FROM blackjack
                WHERE user_id = %s;
                """
        (
            amount_of_games,
            total_bet,
            total_payout,
            winning_amount,
            losing_amount,
        ) = database.select_query(query, (user_id,))[0]

        return {
            "amount_of_games": amount_of_games,
            "total_bet": total_bet,
            "total_payout": total_payout,
            "winning_amount": winning_amount,
            "losing_amount": losing_amount,
        }

    @staticmethod
    def get_total_rows_count():
        query = """
                SELECT SUM(TABLE_ROWS)
                FROM INFORMATION_SCHEMA.TABLES
                """

        return database.select_query_one(query)


class SlotsStats:
    """
    Handles statistics for the /slots command
    """

    def __init__(self, user_id, is_won, bet, payout, spin_type, icons):
        self.user_id = user_id
        self.is_won = is_won
        self.bet = bet
        self.payout = payout
        self.spin_type = spin_type
        self.icons = json.dumps(icons)

    def push(self):
        """
        Insert the services from any given slots game into the database
        """
        query = """
        INSERT INTO slots (user_id, is_won, bet, payout, spin_type, icons)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            self.user_id,
            self.is_won,
            self.bet,
            self.payout,
            self.spin_type,
            self.icons,
        )

        database.execute_query(query, values)

    @staticmethod
    def get_user_stats(user_id):
        """
        Retrieve the Slots stats for a given user from the database.
        """
        query = """
        SELECT
            COUNT(*) AS amount_of_games,
            SUM(bet) AS total_bet,
            SUM(payout) AS total_payout,
            SUM(CASE WHEN spin_type = 'pair' AND is_won = 1 THEN 1 ELSE 0 END) AS games_won_pair,
            SUM(CASE WHEN spin_type = 'three_of_a_kind' AND is_won = 1 THEN 1 ELSE 0 END) AS games_won_three_of_a_kind,
            SUM(CASE WHEN spin_type = 'three_diamonds' AND is_won = 1 THEN 1 ELSE 0 END) AS games_won_three_diamonds,
            SUM(CASE WHEN spin_type = 'jackpot' AND is_won = 1 THEN 1 ELSE 0 END) AS games_won_jackpot
        FROM slots
        WHERE user_id = %s
        """

        (
            amount_of_games,
            total_bet,
            total_payout,
            games_won_pair,
            games_won_three_of_a_kind,
            games_won_three_diamonds,
            games_won_jackpot,
        ) = database.select_query(query, (user_id,))[0]

        return {
            "amount_of_games": amount_of_games,
            "total_bet": total_bet,
            "total_payout": total_payout,
            "games_won_pair": games_won_pair,
            "games_won_three_of_a_kind": games_won_three_of_a_kind,
            "games_won_three_diamonds": games_won_three_diamonds,
            "games_won_jackpot": games_won_jackpot,
        }
