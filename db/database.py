import sqlite3
from sqlite3 import Error


def create_connection():
    try:
        conn = sqlite3.connect("db/rcu.db")
    except Error as e:
        print("'create_connection()' Error occurred: {}".format(e))
        return

    return conn


def execute_query(query, values=None):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)

        conn.commit()
    except Error as e:
        print("'execute_query()' Error occurred: {}".format(e))

    return cursor


def select_query(query, values=None):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        if values:
            return cursor.execute(query, values).fetchall()
        else:
            return cursor.execute(query).fetchall()

    except Error as e:
        return f"ERROR: {e}"


def select_query_one(query, values=None):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        if values:
            output = cursor.execute(query, values).fetchone()
        else:
            output = cursor.execute(query).fetchone()

        if output:
            return output[0]

        return None

    except Error as e:
        return f"ERROR: {e}"
