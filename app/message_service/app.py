import logging, os
from flask import Flask, request, jsonify, g
from flask.views import MethodView
from flasgger import Swagger

from message_service.logic.concrete_message_service import ConcreteMessageService
from foundations.admin.token.get_user_id_from_token import jwt_token_required

ROOTDIR = os.path.dirname(__file__)

class MessageView(MethodView):

    def __init__(self):
        self.message_service_logic = ConcreteMessageService(ROOTDIR)

    @jwt_token_required()
    def get(self):
        """
        This endpoint retrieves all messages
        ---
        responses:
          200:
            description: Returns a list of messages
        """
        try:
            messages = self.message_service_logic.view_messages()
            return jsonify(messages), 200
        except Exception as e:
            logging.error(f"Error getting message: {e}")
            return jsonify({"error": "Server error"}), 500

    @jwt_token_required()
    def post(self):
        """
        This endpoint posts a new message
        ---
        parameters:
        - in: body
          name: body
          schema:
            id: UserMessage
            required:
              - user_id
              - message
            properties:
              user_id:
                type: string
                description: The user's ID
              message:
                type: string
                description: The message text
        responses:
          201:
            description: Message created
        """
        data = request.json
        try:
            message_id = self.message_service_logic.create_message(data['user_id'], data['message'])
            return jsonify({'message_id': message_id}), 201
        except Exception as e:
            logging.error(f"Error posting message: {e}")
            return jsonify({"error": "Server error"}), 500

    @jwt_token_required(require_user_id=True)
    def get_user_messages(self):
        """
        This endpoint retrieves all messages from a specific user
        ---
        responses:
          200:
            description: Returns a list of messages from the user with their vote count
        """
        user_id = g.get('user_id')
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401
        try:
            messages = self.message_service_logic.view_user_messages(user_id)
            return jsonify(messages), 200
        except Exception as e:
            logging.error(f"Error getting user's messages: {e}")
            return jsonify({"error": "Server error"}), 500

    @jwt_token_required(require_user_id=True)
    def delete(self, message_id):
        """
        This endpoint deletes a specific message
        ---
        parameters:
        - in: path
          name: message_id
          type: string
          required: true
          description: The ID of the message to delete
        responses:
          200:
            description: Message deleted
        """
        user_id = g.get('user_id')
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401
        try:
            self.message_service_logic.delete_message(user_id, message_id)
            return jsonify({'status': 'Message deleted'}), 200
        except Exception as e:
            logging.error(f"Error deleting message: {e}")
            return jsonify({"error": "Server error"}), 500

class PingView(MethodView):
    def get(self):
        """
        Just ping the server
        This endpoint does nothing
        ---
        responses:
            200:
                description: Server responded with a pong
        """
        return 'pong', 200

if __name__=="__main__":
    app = Flask(__name__)
    Swagger(app)
    message_service_logic = ConcreteMessageService(ROOTDIR)
    app.config['SECRET_KEY'] = message_service_logic.secret_key

    message_view = MessageView.as_view('message_view')
    ping_view = PingView.as_view('ping_view')

    app.add_url_rule('/messages', view_func=message_view, methods=['GET', 'POST'])
    app.add_url_rule('/user/messages', view_func=message_view, methods=['GET'])
    app.add_url_rule('/messages/<message_id>', view_func=message_view, methods=['DELETE'])
    app.add_url_rule('/ping', view_func=ping_view, methods=['GET'])

    app.run(host='0.0.0.0', port=5000, debug=True)
