from __future__ import annotations

import logging
from typing import Any
from typing import List
from typing import Tuple

import mysql.connector


class DatabaseClient:
    def __init__(self, db_config: dict):
        self.db_config = db_config
        self.db_connection = None
        self.db_cursor = None
        self._check_connection()

    def _check_connection(self):
        try:
            self.connect()
        except Exception as e:
            logging.error(f"Failed to connect to the database: {e}")
            raise

    def connect(self):
        try:
            self.db_connection = mysql.connector.connect(**self.db_config)
            self.db_cursor = self.db_connection.cursor(buffered=True)
            logging.info("Connected to the database")
        except mysql.connector.Error as err:
            logging.error(f"Error connecting to the database: {err}")
            raise

    def disconnect(self):
        try:
            if self.db_cursor:
                self.db_cursor.close()
            if self.db_connection:
                self.db_connection.close()
            logging.info("Disconnected from the database")
        except mysql.connector.Error as err:
            logging.error(f"Error disconnecting from the database: {err}")
            raise

    def execute_query(self, table_name: str, query: str, *args: Any) -> List[Tuple[Any]]:
        try:
            self.connect()
            full_query = query.format(table_name)
            self.db_cursor.execute(full_query, args)

            # If the operation is not a SELECT operation, commit and return None
            if "SELECT" not in full_query.upper():
                self.db_connection.commit()
                return

            # Else fetch results
            result = self.db_cursor.fetchall()
            self.db_connection.commit()
            return result

        except mysql.connector.Error as err:
            self.db_connection.rollback()
            logging.error(f"Error executing query: {err}")
            raise
        finally:
            self.disconnect()

    def get_last_insert_id(self) -> int:
        try:
            self.connect()
            self.db_cursor.execute("SELECT LAST_INSERT_ID()")
            last_id = self.db_cursor.fetchone()[0]
            self.db_connection.commit()
            return last_id
        except mysql.connector.Error as err:
            self.db_connection.rollback()
            logging.error(f"Error retrieving last insert id: {err}")
            raise
        finally:
            self.disconnect()
