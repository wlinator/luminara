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
        if not cash_balance or not special_balance:
            query = """
            INSERT INTO currency (user_id, cash_balance, special_balance)
            VALUES (?, 50, 3)
            """
            database.execute_query(query, (user_id,))
            return 50, 3

        return cash_balance, special_balance
