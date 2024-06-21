from loguru import logger
import os

import mariadb


def create_connection_pool(name: str, size: int) -> mariadb.ConnectionPool:
    pool = mariadb.ConnectionPool(
        host="db",
        port=3306,
        database=os.environ.get("MARIADB_DATABASE"),
        user=os.environ.get("MARIADB_USER"),
        password=os.environ.get("MARIADB_PASSWORD"),
        pool_name=name,
        pool_size=size
    )

    return pool


try:
    _cnxpool = create_connection_pool("core-pool", 25)
except mariadb.Error as e:
    logger.critical(f"Couldn't create the MariaDB connection pool: {e}")
    raise e


def execute_query(query, values=None):
    conn = _cnxpool.get_connection()
    cursor = conn.cursor()

    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)

    conn.commit()
    conn.close()
    return cursor


def select_query(query, values=None):
    conn = _cnxpool.get_connection()
    cursor = conn.cursor()

    if values:
        cursor.execute(query, values)
        output = cursor.fetchall()
    else:
        cursor.execute(query)
        output = cursor.fetchall()

    conn.close()
    return output


def select_query_one(query, values=None):
    conn = _cnxpool.get_connection()
    cursor = conn.cursor()

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
