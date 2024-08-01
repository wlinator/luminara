import mysql.connector
from loguru import logger
from mysql.connector import pooling
import os
import pathlib
import re

from lib.constants import CONST


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


def select_query_dict(query, values=None):
    with _cnxpool.get_connection() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, values)
            return cursor.fetchall()


def run_migrations():
    migrations_dir = "db/migrations"
    migration_files = sorted(
        [f for f in os.listdir(migrations_dir) if f.endswith(".sql")],
    )

    with _cnxpool.get_connection() as conn:
        with conn.cursor() as cursor:
            # Create migrations table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS migrations (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    filename VARCHAR(255) NOT NULL,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            for migration_file in migration_files:
                # Check if migration has already been applied
                cursor.execute(
                    "SELECT COUNT(*) FROM migrations WHERE filename = %s",
                    (migration_file,),
                )
                if cursor.fetchone()[0] > 0:
                    logger.debug(
                        f"Migration {migration_file} already applied, skipping.",
                    )
                    continue

                # Read and execute migration file
                migration_sql = pathlib.Path(
                    os.path.join(migrations_dir, migration_file),
                ).read_text()
                try:
                    # Split the migration file into individual statements
                    statements = re.split(r";\s*$", migration_sql, flags=re.MULTILINE)
                    for statement in statements:
                        if statement.strip():
                            cursor.execute(statement)

                    # Record successful migration
                    cursor.execute(
                        "INSERT INTO migrations (filename) VALUES (%s)",
                        (migration_file,),
                    )
                    conn.commit()
                    logger.debug(f"Successfully applied migration: {migration_file}")
                except mysql.connector.Error as e:
                    conn.rollback()
                    logger.error(f"Error applying migration {migration_file}: {e}")
                    raise

    logger.debug("All migrations completed.")
