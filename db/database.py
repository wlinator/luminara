import logging
import sqlite3
from sqlite3 import Error

racu_logs = logging.getLogger('Racu.Core')


def create_connection():
    try:
        conn = sqlite3.connect("db/rcu.db")
    except Error as e:
        racu_logs.error("'create_connection()' Error occurred: {}".format(e))
        return

    return conn


def execute_query(query, values=None):
    conn = create_connection()
    cursor = conn.cursor()

    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)

    conn.commit()
    return cursor


def select_query(query, values=None):
    conn = create_connection()
    cursor = conn.cursor()

    if values:
        return cursor.execute(query, values).fetchall()
    else:
        return cursor.execute(query).fetchall()


def select_query_one(query, values=None):
    conn = create_connection()
    cursor = conn.cursor()

    if values:
        output = cursor.execute(query, values).fetchone()
    else:
        output = cursor.execute(query).fetchone()

    if output:
        return output[0]

    return None
