from __future__ import annotations

import os

import requests
from flasgger import Swagger
from flask import Flask
from flask import jsonify
from flask import request

from api_gateway.logic.concrete_api_gateway_service import ConcreteApiGatewayService

ROOTDIR = os.path.dirname(__file__)


class ApiGatewayApplication:
    def __init__(self):
        self.app = Flask(__name__)
        self.service = ConcreteApiGatewayService(ROOTDIR)

        self.app.add_url_rule("/ping", "ping", self.ping, methods=["GET"])
        self.app.add_url_rule(
            "/users/<path:path>",
            "user_service",
            self.user_service,
            methods=["GET", "POST", "PUT", "DELETE"],
        )
        self.app.add_url_rule(
            "/messages/<path:path>",
            "message_service",
            self.message_service,
            methods=["GET", "POST", "PUT", "DELETE"],
        )

        @self.app.errorhandler(400)
        def bad_request(error):
            return jsonify(error="Bad request"), 400

        @self.app.errorhandler(404)
        def not_found(error):
            return jsonify(error="Not found"), 404

        @self.app.errorhandler(500)
        def server_error(error):
            return jsonify(error="Internal server error"), 500

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

    def user_service(self, path):
        """
        Forward the request to the user service
        ---
        parameters:
            - in: path
              name: path
              type: string
              required: true
              description: the path to forward to the user service
        responses:
            200:
                description: the request was successfully forwarded to the user service
            400:
                description: the request was not correctly formed
            404:
                description: the requested resource could not be found
            500:
                description: an internal error occurred while processing the request
        """
        return self.send_request(self.service.USER_SERVICE, path)

    def message_service(self, path):
        """
        Forward the request to the message service
        ---
        parameters:
            - in: path
              name: path
              type: string
              required: true
              description: the path to forward to the message service
        responses:
            200:
                description: the request was successfully forwarded to the message service
            400:
                description: the request was not correctly formed
            404:
                description: the requested resource could not be found
            500:
                description: an internal error occurred while processing the request
        """
        return self.send_request(self.service.MESSAGE_SERVICE, path)

    def send_request(self, service_url, path):
        url = f"{service_url}/{path}"

        response = requests.request(
            method=request.method,
            url=url,
            headers={key: value for (key, value) in request.headers if key != "Host"},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
        )

        response_data = ""
        if response.content:
            response_data = response.content.decode("utf-8")

        headers = [(name, value) for (name, value) in response.raw.headers.items()]

        response = self.app.response_class(response=response_data, status=response.status_code, headers=dict(headers))
        return response


if __name__ == "__main__":
    app = ApiGatewayApplication()
    app.run()
