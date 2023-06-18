from __future__ import annotations

import datetime
import logging

import jwt
from authentication_service.logic.auth_service_logic import AbstractAuthService
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


class ConcreteAuthServiceLogic(AbstractAuthService):
    def register(self, username: str, password: str) -> str:
        hached_password = generate_password_hash(str(password), method="sha256")

        query = self.query_builder.select_where("users", {"username": username})
        try:
            user_data = self.db_client.execute_query("users", query)
        except Exception as e:
            logging.exception(f"Failed to retrieve user {username}: {e}")
            return f"Failed to register user {username}. Could not retrieve user data. {e}"

        if user_data and len(user_data) > 0:
            user_id = user_data[0][0]

            query = self.query_builder.update(self.database).set("password_hash = %s").where("user_id = %s").build()
            args = (hached_password, user_id)

            try:
                self.db_client.execute_query(self.database, query, *args)
            except Exception as e:
                logging.exception(f"Failed to update password hash for user {username}: {e}")
                return f"Failed to register user {username}. Could not update password hash. {e}"

            logging.info(f"User {username} registered successfully")
            return f"User {username} registered successfully"
        else:
            return f"Failed to register user {username}. User does not exist."

    def login(self, username: str, password: str) -> str:
        query = self.query_builder.select_where("users", {"username": username})
        try:
            user_data = self.db_client.execute_query("users", query)
        except Exception as e:
            logging.exception(f"Failed to retrieve user {username}: {e}")
            return f"Failed to login. Could not retrieve user data for {username}. {e}"

        query = self.query_builder.select_where(self.database, {"user_id": user_data[0][0]})
        try:
            auth_data = self.db_client.execute_query(self.database, query)
        except Exception as e:
            logging.exception(f"Failed to retrieve user {username} from auth data: {e}")
            return f"Failed to login. Could not retrieve user data for {username}. {e}"

        if user_data and check_password_hash(auth_data[0][3], user_data[0][1]):
            payload = {
                "username": username,
                "user_id": user_data[0][0],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            }
            token = jwt.encode(payload, self.secret_key, algorithm="HS256")

            return token
        else:
            return False

    def logout(self, jti: str) -> str:
        # This function can be used to blacklist or mark the given jti (JWT id) as invalid.
        # For simplicity, we return a success message.
        return "User logged out successfully"
