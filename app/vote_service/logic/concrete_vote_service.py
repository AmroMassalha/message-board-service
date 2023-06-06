import logging

from vote_service.logic.vote_service_logic import AbstractVoteService

class ConcreteVoteService(AbstractVoteService):

    def vote_message(self, user_id: str, message_id: str, vote_type: str) -> None:
        if vote_type in ['up', 'down']:
            vote_data = (user_id, message_id, vote_type)
            query = (self.query_builder
                        .insert_into(self.database, "user_id, message_id, vote_type", vote_data)
                        .on_duplicate_key_update("vote_type = VALUES(vote_type)")
                        .build())
            try:
                self.db_client.execute_query(self.database, query, vote_data)
                logging.info(f"User {user_id} voted '{vote_type}' for message {message_id}")
            except Exception as e:
                logging.error(f"Error while voting: {e}")
                raise
        else:
            logging.error("Invalid vote type. It should be either 'up' or 'down'.")
            raise ValueError("Invalid vote type. It should be either 'up' or 'down'.")
