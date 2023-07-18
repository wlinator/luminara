import locale

from db import database


class Currency:
    def __init__(self, user_id):
        self.user_id = user_id
        (self.cash, self.special) = Currency.fetch_or_create_balance(self.user_id)

    def add_cash(self, amount):
        self.cash += abs(amount)

    def add_special(self, amount):
        self.special += abs(amount)

    def take_cash(self, amount):
        self.cash -= abs(amount)

        if self.cash < 0:
            self.cash = 0

    def take_special(self, amount):
        self.special -= abs(amount)

        if self.special < 0:
            self.special = 0

    def push(self):
        query = """
        UPDATE currency
        SET cash_balance = ?, special_balance = ?
        WHERE user_id = ?
        """

        database.execute_query(query, (round(self.cash), round(self.special), self.user_id))

    @staticmethod
    def fetch_or_create_balance(user_id):
        query = """
        SELECT cash_balance, special_balance
        FROM currency
        WHERE user_id = ?
        """

        try:
            (cash_balance, special_balance) = database.select_query(query, (user_id,))[0]
        except (IndexError, TypeError):
            (cash_balance, special_balance) = (None, None)

        # if the user doesn't have a balance yet -> create one
        # additionally if for some reason a balance becomes Null
        # re-generate the user's balance as fallback.
        if cash_balance is None or special_balance is None:
            query = """
            INSERT INTO currency (user_id, cash_balance, special_balance)
            VALUES (?, 50, 3)
            """
            database.execute_query(query, (user_id,))
            return 50, 3

        return cash_balance, special_balance

    @staticmethod
    def load_leaderboard():
        query = "SELECT user_id, cash_balance FROM currency ORDER BY cash_balance DESC"
        data = database.select_query(query)

        leaderboard = []
        rank = 1
        for row in data:
            row_user_id = row[0]
            cash_balance = row[1]
            leaderboard.append((row_user_id, cash_balance, rank))
            rank += 1

        return leaderboard

    @staticmethod
    def format(num):
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        return locale.format_string("%d", num, grouping=True)

    @staticmethod
    def format_human(num):
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0

        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
