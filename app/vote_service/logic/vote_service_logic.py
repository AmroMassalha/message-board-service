from typing import List, Dict, Any
from abc import ABC, abstractmethod

from foundations.database.database_client import DatabaseClient
from foundations.config_reader.config_reader import ConfigReader
from foundations.database.query_builder import QueryBuilder

class AbstractVoteService(ABC):
    def __init__(self, root_dir: str):
        self.config_reader = ConfigReader(root_dir)
        self.config = None
        try:
            self.config = self.config_reader.get_config()
        except Exception as e:
            print(f"Error while reading config: {e}")
            raise

        if self.config:
            self.message_srv_endpoint = self.config.get('MESSAGE_SERVICE', {})
            self.secret_key = self.config.get("APP_SECRET_KEY", {})
            db_config = self.config.get('db_config', {}).copy()
            self.database = db_config.get('table')
            if not self.database:
                raise ValueError("'table' key not found in the database configuration")
            db_config.pop('table')
            self.db_client = DatabaseClient(db_config)
            self.query_builder = QueryBuilder()

    @abstractmethod
    def vote_message(self, user_id: str, message_id: str, vote_type: str) -> None:
        """
        Allows a user to vote on a message
        :param user_id: ID of the user voting
        :param message_id: ID of the message to vote for
        :param vote_type: Type of vote ('up' or 'down')
        :return: None
        """
        pass
