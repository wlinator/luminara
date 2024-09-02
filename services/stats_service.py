import json

from db import database


class BlackJackStats:
    def __init__(
        self,
        user_id: int,
        is_won: bool,
        bet: int,
        payout: int,
        hand_player: list[str],
        hand_dealer: list[str],
    ):
        self.user_id: int = user_id
        self.is_won: bool = is_won
        self.bet: int = bet
        self.payout: int = payout
        self.hand_player: str = json.dumps(hand_player)
        self.hand_dealer: str = json.dumps(hand_dealer)

    def push(self) -> None:
        query: str = """
        INSERT INTO blackjack (user_id, is_won, bet, payout, hand_player, hand_dealer)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values: tuple[int, bool, int, int, str, str] = (
            self.user_id,
            self.is_won,
            self.bet,
            self.payout,
            self.hand_player,
            self.hand_dealer,
        )

        database.execute_query(query, values)

    @staticmethod
    def get_user_stats(user_id: int) -> dict[str, int]:
        query: str = """
                SELECT
                    COUNT(*) AS amount_of_games,
                    SUM(bet) AS total_bet,
                    SUM(payout) AS total_payout,
                    SUM(CASE WHEN is_won = 1 THEN 1 ELSE 0 END) AS winning,
                    SUM(CASE WHEN is_won = 0 THEN 1 ELSE 0 END) AS losing
                FROM blackjack
                WHERE user_id = %s;
                """
        result: tuple[int, int, int, int, int] = database.select_query(query, (user_id,))[0]
        (
            amount_of_games,
            total_bet,
            total_payout,
            winning_amount,
            losing_amount,
        ) = result

        return {
            "amount_of_games": amount_of_games,
            "total_bet": total_bet,
            "total_payout": total_payout,
            "winning_amount": winning_amount,
            "losing_amount": losing_amount,
        }

    @staticmethod
    def get_total_rows_count() -> int:
        query: str = """
                SELECT SUM(TABLE_ROWS)
                FROM INFORMATION_SCHEMA.TABLES
                """

        result = database.select_query_one(query)
        return int(result) if result is not None else 0


class SlotsStats:
    """
    Handles statistics for the /slots command
    """

    def __init__(self, user_id: int, is_won: bool, bet: int, payout: int, spin_type: str, icons: list[str]):
        self.user_id: int = user_id
        self.is_won: bool = is_won
        self.bet: int = bet
        self.payout: int = payout
        self.spin_type: str = spin_type
        self.icons: str = json.dumps(icons)

    def push(self) -> None:
        """
        Insert the services from any given slots game into the database
        """
        query: str = """
        INSERT INTO slots (user_id, is_won, bet, payout, spin_type, icons)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values: tuple[int, bool, int, int, str, str] = (
            self.user_id,
            self.is_won,
            self.bet,
            self.payout,
            self.spin_type,
            self.icons,
        )

        database.execute_query(query, values)

    @staticmethod
    def get_user_stats(user_id: int) -> dict[str, int]:
        """
        Retrieve the Slots stats for a given user from the database.
        """
        query: str = """
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

        result: tuple[int, int, int, int, int, int, int] = database.select_query(query, (user_id,))[0]
        (
            amount_of_games,
            total_bet,
            total_payout,
            games_won_pair,
            games_won_three_of_a_kind,
            games_won_three_diamonds,
            games_won_jackpot,
        ) = result

        return {
            "amount_of_games": amount_of_games,
            "total_bet": total_bet,
            "total_payout": total_payout,
            "games_won_pair": games_won_pair,
            "games_won_three_of_a_kind": games_won_three_of_a_kind,
            "games_won_three_diamonds": games_won_three_diamonds,
            "games_won_jackpot": games_won_jackpot,
        }
