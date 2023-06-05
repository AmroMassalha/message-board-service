from typing import List, Dict, Any
from abc import ABC, abstractmethod

from foundations.database.database_client import DatabaseClient
from foundations.config_reader.config_reader import ConfigReader
from foundations.database.query_builder import QueryBuilder

class AbstractMessageService(ABC):
    _instance = None
    database = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AbstractMessageService, cls).__new__(cls)
        return cls._instance

    def __init__(self, root_dir: str):
        if not self.database:
            self.config_reader = ConfigReader(root_dir)
            self.config = self.config_reader.get_config()
            self.vote_srv_endpoint = self.config.get('VOTE_SERVICE', {})
            self.secret_key = self.config.get("APP_SECRET_KEY")
            self.db_config = self.config.get('db_config', {})
            self.database = self.db_config.pop('table')
            self.db_client = DatabaseClient(self.db_config)
            self.query_builder = QueryBuilder()

    @abstractmethod
    def create_message(self, user_id: str, message_content: str) -> str:
        """
        Creates a new message by a user
        :param user_id: ID of the user creating the message
        :param message_content: Content of the message
        :return: ID of the created message
        """
        pass

    @abstractmethod
    def view_messages(self) -> List[Dict[str, Any]]:
        """
        Returns all the messages currently posted on the message board
        :return: List of dictionaries with details of each message
        """
        pass

    @abstractmethod
    def vote_message(self, user_id: str, message_id: str, vote_type: str) -> int:
        """
        Allows a user to vote on a message
        :param user_id: ID of the user voting
        :param message_id: ID of the message to vote for
        :param vote_type: Type of vote ('up' or 'down')
        :return: Updated vote count of the message
        """
        pass

    @abstractmethod
    def delete_message(self, user_id: str, message_id: str) -> None:
        """
        Deletes a user's message
        :param user_id: ID of the user deleting the message
        :param message_id: ID of the message to delete
        :return: None
        """
        pass

    @abstractmethod
    def view_user_messages(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Returns all messages posted by a user
        :param user_id: ID of the user whose messages to retrieve
        :return: List of dictionaries with details of each message posted by the user
        """
        pass
