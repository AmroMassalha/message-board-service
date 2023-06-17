from __future__ import annotations

import logging

from vote_service.logic.vote_service_logic import AbstractVoteService


class ConcreteVoteService(AbstractVoteService):
    def update_vote(self, user_id: str, message_id: str, vote_type: str) -> bool:
        if vote_type not in ["up", "down"]:
            logging.error("Invalid vote type. It should be either 'up' or 'down'.")
            raise ValueError("Invalid vote_type. It should be either 'up' or 'down'.")

        # Check if the vote exists
        check_query = self.query_builder.select(self.database, "*", "user_id = %s AND message_id = %s")
        result = self.db_client.execute_query(self.database, check_query, (user_id, message_id))

        if not result:
            logging.error(f"No existing vote from user {user_id} for message {message_id}")
            return False

        # If the vote exists, update it
        update_data = (vote_type, user_id, message_id)
        update_query = self.query_builder.update(self.database, "vote_type = %s", "user_id = %s AND message_id = %s")
        try:
            self.db_client.execute_query(self.database, update_query, update_data)
            logging.info(f"User {user_id} changed vote to '{vote_type}' for message {message_id}")
            return True
        except Exception as e:
            logging.error(f"Error while updating vote: {e}")
            raise
