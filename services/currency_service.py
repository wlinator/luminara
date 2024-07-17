import locale

from db import database


class Currency:
    def __init__(self, user_id):
        self.user_id = user_id
        self.balance = Currency.fetch_or_create_balance(self.user_id)

    def add_balance(self, amount):
        self.balance += abs(amount)

    def take_balance(self, amount):
        self.balance -= abs(amount)

        if self.balance < 0:
            self.balance = 0

    def push(self):
        query = """
        UPDATE currency
        SET balance = %s
        WHERE user_id = %s
        """

        database.execute_query(query, (round(self.balance), self.user_id))

    @staticmethod
    def fetch_or_create_balance(user_id):
        query = """
        SELECT balance
        FROM currency
        WHERE user_id = %s
        """

        try:
            balance = database.select_query_one(query, (user_id,))
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
    def load_leaderboard():
        query = "SELECT user_id, balance FROM currency ORDER BY balance DESC"
        data = database.select_query(query)

        leaderboard = []
        rank = 1
        for row in data:
            row_user_id = row[0]
            balance = row[1]
            leaderboard.append((row_user_id, balance, rank))
            rank += 1

        return leaderboard

    @staticmethod
    def format(num):
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        return locale.format_string("%d", num, grouping=True)

    @staticmethod
    def format_human(num):
        num = float("{:.3g}".format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0

        return "{}{}".format(
            "{:f}".format(num).rstrip("0").rstrip("."),
            ["", "K", "M", "B", "T", "Q", "Qi", "Sx", "Sp", "Oc", "No", "Dc"][
                magnitude
            ],
        )

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
