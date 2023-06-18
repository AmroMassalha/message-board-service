from __future__ import annotations

import logging
from abc import ABC
from abc import abstractmethod

from foundations.config_reader.config_reader import ConfigReader
from foundations.database.database_client import DatabaseClient
from foundations.database.query_builder import QueryBuilder


class AbstractAuthService(ABC):
    def __init__(self, root_dir: str):
        self.config_reader = ConfigReader(root_dir)
        self.config = None
        try:
            self.config = self.config_reader.get_config()
        except Exception as e:
            logging.error(f"Error while reading config: {e}")
            raise

        if self.config:
            self.secret_key = self.config.get("APP_SECRET_KEY")
            self.USER_SERVICE = self.config.get("USER_SERVICE", None)
            db_config = self.config.get("db_config", {}).copy()
            self.database = db_config.get("table")
            if not self.database:
                raise ValueError("'table' key not found in the database configuration")
            db_config.pop("table")
            self.db_client = DatabaseClient(db_config)
            self.query_builder = QueryBuilder()

    @abstractmethod
    def register(self, username: str, password: str) -> bool:
        """
        Creates a new user
        :param username: The username of the user to create
        :param password: The password of the user to create
        :return: Success message
        """
        pass

    @abstractmethod
    def login(self, username: str, password: str) -> str:
        """
        Edits an existing user
        :param user_id: The ID of the user to edit
        :param username: The new username of the user
        :param password: The new password of the user
        :return: Success message
        """
        pass

    @abstractmethod
    def logout(self, jti: str) -> str:
        """
        Deletes an existing user
        :param user_id: The ID of the user to delete
        :return: Success message
        """
        pass
