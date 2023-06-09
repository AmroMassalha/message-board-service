from __future__ import annotations

import logging
import os

from flasgger import Swagger
from flask import Flask
from flask import jsonify
from flask import request
from vote_service.logic.concrete_vote_service import ConcreteVoteService

ROOTDIR = os.path.dirname(__file__)


class VoteServiceApplication:
    def __init__(self):
        self.app = Flask(__name__)
        self.service = ConcreteVoteService(ROOTDIR)

        self.app.add_url_rule("/ping", "ping", self.ping, methods=["GET"])
        self.app.add_url_rule("/vote", "vote_message", self.update_vote, methods=["PATCH"])

        self.swagger = Swagger(self.app)

    def run(self, host="0.0.0.0", port=5000):
        self.app.run(host=host, port=port, debug=True)

    def ping(self):
        """
        Just ping the server
        This endpoint does nothing
        ---
        responses:
            200:
                description: Server responded with a pong
        """
        return "pong", 200

    def update_vote(self):
        """
        Allow logged-in users to update their vote for a message
        This endpoint allows a user to change their vote up or down for a specific message.
        The request should include a user_id, a message_id and a vote_type.
        ---
        parameters:
            - in: body
              name: body
              required: true
              schema:
                type: object
                properties:
                    message_id:
                      type: string
                      description: The ID of the message to change vote for
                    vote_type:
                      type: string
                      description: The type of vote ('up' or 'down')
        responses:
            200:
                description: Vote updated successfully
            400:
                description: Invalid request or vote type
            404:
                description: Vote not found
            500:
                description: Internal server error
        """

        data = request.json
        if not all(key in data for key in ("message_id", "vote_type", "user_id")):
            return jsonify({"error": "Missing required data"}), 400
        message_id = data["message_id"]
        vote_type = data["vote_type"]
        user_id = data["user_id"]

        try:
            updated = self.service.update_vote(user_id, message_id, vote_type)
            if updated:
                return jsonify({"message": "Vote updated successfully"}), 200
            else:
                return jsonify({"error": "Vote not found"}), 404
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logging.error(f"Error updating vote: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app = VoteServiceApplication()
    app.run()
