import logging
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

racu_logs = logging.getLogger('Racu.Core')
load_dotenv('.env')


cnxpool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name='core-pool',
    pool_size=25,
    host='db',
    user=os.getenv("MARIADB_USER"),
    password=os.getenv("MARIADB_PASSWORD"),
    database='racudb'
)


def execute_query(query, values=None):
    conn = cnxpool.get_connection()
    cursor = conn.cursor()

    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)

    conn.commit()
    conn.close()
    racu_logs.debug(f"database.execute_query: 'query': {query}, 'values': {values}")
    return cursor


def select_query(query, values=None):
    conn = cnxpool.get_connection()
    cursor = conn.cursor()

    racu_logs.debug(f"database.select_query: 'query': {query}, 'values': {values}")

    if values:
        cursor.execute(query, values)
        output = cursor.fetchall()
    else:
        cursor.execute(query)
        output = cursor.fetchall()

    conn.close()
    return output


def select_query_one(query, values=None):
    conn = cnxpool.get_connection()
    cursor = conn.cursor()

    racu_logs.debug(f"database.select_query_one: 'query': {query}, 'values': {values}")

    if values:
        cursor.execute(query, values)
        output = cursor.fetchone()
    else:
        cursor.execute(query)
        output = cursor.fetchone()

    conn.close()

    if output:
        return output[0]

    return None
