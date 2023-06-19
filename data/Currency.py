from db import database


class Currency:
    @staticmethod
    def get_cash_balance(user_id):
        query = "SELECT cash_balance FROM currency WHERE user_id={}".format(user_id)
        cash_balance = database.select_query(query)

        if not cash_balance:
            Currency.create_new_balance(user_id)
            return 50

        return cash_balance[0][0]

    @staticmethod
    def get_special_balance(user_id):
        query = "SELECT special_balance FROM currency WHERE user_id={}".format(user_id)
        special_balance = database.select_query(query)

        if not special_balance:
            Currency.create_new_balance(user_id)
            return 3

        return special_balance[0][0]

    @staticmethod
    def update_cash_balance(user_id, amount):
        if amount < 0:
            amount = 0

        query = "UPDATE currency SET cash_balance = {} WHERE user_id = {}".format(round(amount, 2), user_id)
        database.execute_query(query)
        
    @staticmethod
    def update_special_balance(user_id, amount):
        if amount < 0:
            amount = 0

        query = "UPDATE currency SET special_balance = {} WHERE user_id = {}".format(amount, user_id)
        database.execute_query(query)

    @staticmethod
    def create_new_balance(user_id):
        query = "INSERT INTO currency(user_id, cash_balance, special_balance) VALUES ({}, 50, 3)".format(user_id)
        database.execute_query(query)
        print(f"BALANCE UPDATE --- USER with ID {user_id} created new balance")
