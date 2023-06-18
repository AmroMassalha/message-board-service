from __future__ import annotations

import logging
import os

from authentication_service.logic.concrete_auth_service_logic import (
    ConcreteAuthServiceLogic,
)
from flasgger import Swagger
from flask import Flask
from flask import jsonify
from flask import request
from flask_jwt_extended import JWTManager

ROOTDIR = os.path.dirname(__file__)


class AuthServiceApplication:
    def __init__(self):
        self.app = Flask(__name__)
        self.auth_service_logic = ConcreteAuthServiceLogic(ROOTDIR)
        self.jwt = JWTManager(self.app)
        self.app.config["JWT_SECRET_KEY"] = self.auth_service_logic.secret_key

        self.app.add_url_rule("/ping", "ping", self.ping, methods=["GET"])
        self.app.add_url_rule("/register", "register", self.register, methods=["POST"])
        self.app.add_url_rule("/login", "login", self.login, methods=["POST"])
        # self.app.add_url_rule("/logout", "logout", self.logout, methods=["POST"])

        self.swagger = Swagger(self.app)

    def run(self, host="0.0.0.0", port=5000):
        self.app.run(host=host, port=port, debug=True)

    def ping(self):
        """
        just ping the server
        this endpoint does nothing
        ---
        responses:
            200:
                description: server responded with a pong
        """
        return "pong", 200

    def register(self):
        """
        Register a new user
        ---
        parameters:
            - name: body
              in: body
              required: true
              schema:
                id: user
                required:
                    - username
                    - password
                properties:
                    username:
                        type: string
                        description: The user's name
                    password:
                        type: string
                        description: The user's password
        responses:
            200:
                description: User registered successfully
            400:
                description: Invalid request, username and password required
            500:
                description: Error occurred while registering user
        """
        data = request.get_json()
        if not data or "username" not in data or "password" not in data:
            return (
                jsonify({"error": "Invalid request, username and password required"}),
                400,
            )

        try:
            self.auth_service_logic.register(data["username"], data["password"])
            return jsonify({"message": "User registered successfully"}), 200
        except Exception as e:
            logging.error(f"Error registering user: {e}")
            return jsonify({"error": "Error occurred while registering user"}), 500

    def login(self):
        """
        Log in an existing user
        ---
        parameters:
            - name: body
              in: body
              required: true
              schema:
                id: user
                required:
                    - username
                    - password
                properties:
                    username:
                        type: string
                        description: The user's name
                    password:
                        type: string
                        description: The user's password
        responses:
            200:
                description: User logged in successfully
            400:
                description: Invalid request, username and password required
            500:
                description: Error occurred while logging in user
        """
        data = request.get_json()
        if not data or "username" not in data or "password" not in data:
            return (
                jsonify({"error": "Invalid request, username and password required"}),
                400,
            )

        try:
            token = self.auth_service_logic.login(data["username"], data["password"])
            if token:
                return (
                    jsonify({"message": "User logged in successfully", "token": token}),
                    200,
                )
            else:
                return jsonify("Invalid login credentials"), 401
        except Exception as e:
            logging.error(f"Error logging in user: {e}")
            return jsonify({"error": "Error occurred while logging in user"}), 500

    # def logout(self):
    #     """
    #     Log out the current user
    #     ---
    #     responses:
    #         200:
    #             description: User logged out successfully
    #         500:
    #             description: Error occurred while logging out user
    #     """
    #     try:
    #         self.auth_service_logic.logout()
    #         return jsonify({"message": "User logged out successfully"}), 200
    #     except Exception as e:
    #         logging.error(f"Error logging out user: {e}")
    #         return jsonify({"error": "Error occurred while logging out user"}), 500


if __name__ == "__main__":
    app = AuthServiceApplication()
    app.run()
