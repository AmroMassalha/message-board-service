from __future__ import annotations

import logging
from typing import Any
from typing import List
from typing import Tuple

from user_service.logic.user_service_logic import AbstractUserService


class ConcreteUserServiceLogic(AbstractUserService):
    def create_user(self, username: str, password: str) -> str:
        args = (username, password)
        query = self.query_builder.insert_into(self.database, "username, password", args).build()
        try:
            self.db_client.execute_query(self.database, query, *args)
            return "User created successfully"
        except Exception as e:
            logging.error(f"Error creating User: {e}")
            raise

    def edit_user(self, user_id: int, username: str, password: str) -> str:
        query = self.query_builder.update(self.database).set("username = %s, password = %s").where("id = %s").build()
        args = (username, password, user_id)
        try:
            self.db_client.execute_query(self.database, query, *args)
            return "User updated successfully"
        except Exception as e:
            logging.error(f"Error updating user: {e}")
            raise

    def delete_user(self, user_id: int) -> str:
        query = self.query_builder.delete_from(self.database).where("id = %s").build()
        args = (user_id,)
        try:
            self.db_client.execute_query(self.database, query, *args)
            return "User deleted successfully"
        except Exception as e:
            logging.error(f"Error deleting user: {e}")
            raise

    def get_user(self, user_id: int) -> List[Tuple[Any]]:
        query = self.query_builder.select(self.database).where("id = %s").build()
        args = (user_id,)
        try:
            result = self.db_client.execute_query(self.database, query, *args)
            return result
        except Exception as e:
            logging.error(f"Error getting user: {e}")
            raise

    def get_all_user(self) -> List[Tuple[Any]]:
        query = self.query_builder.select(self.database).build()
        try:
            result = self.db_client.execute_query(self.database, query)
            return result
        except Exception as e:
            logging.error(f"Error getting all users: {e}")
            raise

    def get_user_by_username(self, username: str) -> dict or None:
        query = self.query_builder.select(self.database).where("username = %s").build()
        args = (username,)
        try:
            result = self.db_client.execute_query(self.database, query, *args)
            if result:
                return {
                    "id": result[0][0],
                    "username": result[0][1],
                    "password": result[0][2],
                }
            else:
                return None
        except Exception as e:
            logging.error(f"Error getting user by username: {e}")
            raise
