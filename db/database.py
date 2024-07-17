from lib.constants import CONST
from loguru import logger
import mysql.connector
from mysql.connector import pooling


def create_connection_pool(name: str, size: int) -> pooling.MySQLConnectionPool:
    return pooling.MySQLConnectionPool(
        pool_name=name,
        pool_size=size,
        host="db",
        port=3306,
        database=CONST.MARIADB_DATABASE,
        user=CONST.MARIADB_USER,
        password=CONST.MARIADB_PASSWORD,
        charset="utf8mb4",
        collation="utf8mb4_unicode_ci",
    )


try:
    _cnxpool = create_connection_pool("core-pool", 25)
except mysql.connector.Error as e:
    logger.critical(f"Couldn't create the MySQL connection pool: {e}")
    raise e


def execute_query(query, values=None):
    with _cnxpool.get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, values)
            conn.commit()
            return cursor


def select_query(query, values=None):
    with _cnxpool.get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, values)
            return cursor.fetchall()


def select_query_one(query, values=None):
    with _cnxpool.get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, values)
            output = cursor.fetchone()
            return output[0] if output else None
