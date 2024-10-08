import locale

from db import database


class Currency:
    def __init__(self, user_id: int) -> None:
        self.user_id: int = user_id
        self.balance: int = Currency.fetch_or_create_balance(self.user_id)

    def add_balance(self, amount: int) -> None:
        self.balance += abs(amount)

    def take_balance(self, amount: int) -> None:
        self.balance -= abs(amount)
        self.balance = max(self.balance, 0)

    def push(self) -> None:
        query: str = """
        UPDATE currency
        SET balance = %s
        WHERE user_id = %s
        """

        database.execute_query(query, (round(self.balance), self.user_id))

    @staticmethod
    def fetch_or_create_balance(user_id: int) -> int:
        query: str = """
        SELECT balance
        FROM currency
        WHERE user_id = %s
        """

        try:
            balance: int | None = database.select_query_one(query, (user_id,))
        except (IndexError, TypeError):
            balance = None

        # if the user doesn't have a balance yet -> create one
        # additionally if for some reason a balance becomes Null
        # re-generate the user's balance as fallback.
        if balance is None:
            query = """
            INSERT INTO currency (user_id, balance)
            VALUES (%s, 50)
            """
            database.execute_query(query, (user_id,))
            return 50

        return balance

    @staticmethod
    def load_leaderboard() -> list[tuple[int, int, int]]:
        query: str = "SELECT user_id, balance FROM currency ORDER BY balance DESC"
        data: list[tuple[int, int]] = database.select_query(query)

        return [(row[0], row[1], rank) for rank, row in enumerate(data, start=1)]

    @staticmethod
    def format(num: int) -> str:
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        return locale.format_string("%d", num, grouping=True)

    @staticmethod
    def format_human(num: int) -> str:
        num_float: float = float(f"{num:.3g}")
        magnitude: int = 0
        while abs(num_float) >= 1000:
            magnitude += 1
            num_float /= 1000.0

        suffixes: list[str] = ["", "K", "M", "B", "T", "Q", "Qi", "Sx", "Sp", "Oc", "No", "Dc"]
        return f'{f"{num_float:f}".rstrip("0").rstrip(".")}{suffixes[magnitude]}'

        # A Thousand = K
        # Million = M
        # Billion = B
        # Trillion = T
        # Quadrillion: Q
        # Quintillion: Qi
        # Sextillion: Sx
        # Septillion: Sp
        # Octillion: Oc
        # Nonillion: No
        # Decillion: Dc
