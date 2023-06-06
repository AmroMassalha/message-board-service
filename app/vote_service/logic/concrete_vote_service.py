import requests
import logging

from typing import List, Any, Tuple

from vote_service.logic.vote_service_logic import AbstractVoteService

class ConcreteVoteService(AbstractVoteService):

    def vote_message(self, user_id, message_id, vote_type):
        pass
