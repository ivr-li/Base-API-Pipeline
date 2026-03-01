from contextlib import contextmanager
from datetime import date

from psycopg2 import OperationalError, connect

from src.config import config
from src.logger import logger_critical


class DB:
    def __init__(self):
        """Initialize the database connection"""
        self.conn = self._create_connection()

    def close(self):
        self.conn.close()

    @contextmanager
    def _context_manager(self):
        """Context manager for database transactions"""
        cur = self.conn.cursor()
        try:
            yield cur
            self.conn.commit()
        finally:
            cur.close()

    def _create_connection(self):
        """Connect to PostgreSQL"""
        if not config.DB:
            logger_critical.critical("Database connection string is not set")
            raise SystemExit(1)

        try:
            return connect(config.DB)
        except OperationalError as ex:
            logger_critical.critical(f"Database connection failed:{ex}")
            raise SystemExit(1)

    def create_table(self):
        """Create project tables"""
        with self._context_manager() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS requests (
                    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    base_code VARCHAR(3) NOT NULL,
                    request_status VARCHAR(20) NOT NULL
                );
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS rates (
                    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    request_id INTEGER NOT NULL,
                    date DATE NOT NULL,
                    rate_code VARCHAR(3) NOT NULL,
                    rate NUMERIC(16,4) NOT NULL,
                    FOREIGN KEY (request_id) REFERENCES requests(id)
                );
                """
            )

    def _insert_request(self, base_code: str, request_status: str) -> int:
        """Insert a new request and return its ID"""
        with self._context_manager() as cur:
            cur.execute(
                """
                INSERT INTO requests (base_code, request_status)
                VALUES (%s, %s)
                RETURNING id
                """,
                (base_code, request_status),
            )

            return cur.fetchone()[0]

    def _insert_rates(self, request_id: int, date: date, rates: dict):
        """Insert rates for a given request"""
        with self._context_manager() as cur:
            values = [(request_id, date, code, rate) for code, rate in rates.items()]

            cur.executemany(
                """
                INSERT INTO rates (request_id, date, rate_code, rate)
                VALUES (%s, %s, %s, %s)
                """,
                values,
            )

    def _drop_tables(self):
        """Drop all tables"""
        with self._context_manager() as cur:
            cur.execute("DROP TABLE IF EXISTS rates, requests CASCADE;")
