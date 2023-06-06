import logging
from typing import List, Tuple, Any
from abc import ABC, abstractmethod

from foundations.database.database_client import DatabaseClient
from foundations.config_reader.config_reader import ConfigReader
from foundations.database.query_builder import QueryBuilder

class AbstractUserService(ABC):
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
            db_config = self.config.get('db_config', {}).copy()
            self.database = db_config.get("table")
            if not self.database:
                raise ValueError("'table' key not found in the database configuration")
            db_config.pop('table')
            self.db_client = DatabaseClient(db_config)
            self.query_builder = QueryBuilder()

    @abstractmethod
    def create_user(self, username: str, password: str) -> str:
        """
        Creates a new user
        :param username: The username of the user to create
        :param password: The password of the user to create
        :return: Success message
        """
        pass

    @abstractmethod
    def edit_user(self, user_id: int, username: str, password: str) -> str:
        """
        Edits an existing user
        :param user_id: The ID of the user to edit
        :param username: The new username of the user
        :param password: The new password of the user
        :return: Success message
        """
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> str:
        """
        Deletes an existing user
        :param user_id: The ID of the user to delete
        :return: Success message
        """
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> List[Tuple[Any]]:
        """
        Retrieves a user by ID
        :param user_id: The ID of the user to retrieve
        :return: A list of tuples representing the user data
        """
        pass

    @abstractmethod
    def get_all_user(self) -> List[Tuple[Any]]:
        """
        Retrieves all users
        :return: A list of tuples each representing a user data
        """
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> List[Tuple[Any]]:
        """
        Retrieves a user by username
        :param username: The username of the user to retrieve
        :return: A list of tuples representing the user data
        """
        pass
