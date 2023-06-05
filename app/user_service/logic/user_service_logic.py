from typing import List, Tuple, Any
from abc import ABC, abstractmethod

from foundations.database.database_client import DatabaseClient
from foundations.config_reader.config_reader import ConfigReader
from foundations.database.query_builder import QueryBuilder

class UserServiceLogic(ABC):
    def __init__(self, root_dir: str):
        self.config_reader = ConfigReader(root_dir)
        self.config = self.config_reader.get_config()
        self.auth_srv_endpoint = self.config.get('AUTH_SERVICE', {})
        self.db_config = self.config.get('db_config', {})
        self.database = self.db_config.pop("table")  # Specify the table name here
        self.db_client = DatabaseClient(self.db_config)
        self.query_builder = QueryBuilder()

    @abstractmethod
    def create_user(self, username: str, password: str) -> str:
        pass

    @abstractmethod
    def edit_user(self, user_id: int, username: str, password: str) -> str:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> str:
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> List[Tuple[Any]]:
        pass

    @abstractmethod
    def get_all_user(self) -> List[Tuple[Any]]:
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> List[Tuple[Any]]:
        pass
