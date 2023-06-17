from __future__ import annotations

import logging
from typing import Any
from typing import List
from typing import Tuple

import requests

from message_service.logic.message_service_logic import AbstractMessageService


class ConcreteMessageService(AbstractMessageService):
    def create_message(self, user_id: str, message: str) -> str:
        query = self.query_builder.insert(self.database, {"user_id": user_id, "message": message})
        try:
            self.db_client.execute_query(self.database, query)
            return str(self.db_client.db_cursor.lastrowid)
        except Exception as e:
            logging.error(f"Error while creating message: {str(e)}")
            raise

    def view_messages(self) -> List[Tuple[Any]]:
        try:
            query = self.query_builder.select_all(self.database)
            return self.db_client.execute_query(self.database, query)
        except Exception as e:
            logging.error(f"Error while viewing messages: {str(e)}")
            raise

    def vote_message(self, user_id: str, message_id: str, vote_type: str) -> int:
        try:
            response = requests.put(
                f"{self.vote_srv_endpoint}/vote",
                json={
                    "user_id": user_id,
                    "message_id": message_id,
                    "vote_type": vote_type,
                },
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Error while voting for message: {str(e)}")
            raise

    def delete_message(self, user_id: str, message_id: str) -> None:
        try:
            query = self.query_builder.delete(self.database, {"user_id": user_id, "message_id": message_id})

            self.db_client.execute_query(self.database, query)
        except Exception as e:
            logging.error(f"Error while deleting message: {str(e)}")
            raise

    def view_user_messages(self, user_id: str) -> List[Tuple[Any]]:
        try:
            query = self.query_builder.select_where(self.database, {"user_id": user_id})
            return self.db_client.execute_query(self.database, query)
        except Exception as e:
            logging.error(f"Error while viewing user messages: {str(e)}")
            raise

    def check_vote_service_health(self) -> bool:
        try:
            response = requests.get(f"{self.vote_srv_endpoint}/ping")
            response.raise_for_status()
            return True
        except Exception as e:
            logging.error(f"Error while checking vote service health: {str(e)}")
            return False
