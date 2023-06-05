import logging, os
from flasgger import Swagger
from flask import Flask, jsonify, request, abort
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash

from foundations.admin.secrer_key_generator import SecretKeyGenerator
from user_service.logic.concrete_user_service_logic import ConcreteUserServiceLogic

ROOTDIR = os.path.dirname(__file__) 

class UserServiceApplication:
    _key_generator = SecretKeyGenerator()
    BLACKLIST = set()

    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['JWT_SECRET_KEY'] = self._key_generator.generate_key()
        self.app.config['JWT_BLACKLIST_ENABLED'] = True
        self.app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
        self.jwt = JWTManager(self.app)
        self.user_service_logic = ConcreteUserServiceLogic(ROOTDIR)

        self.app.add_url_rule('/ping', 'ping', self.ping, methods=['GET'])
        self.app.add_url_rule("/users", "get_all_users", self.get_all_users, methods=["GET"])
        self.app.add_url_rule("/users/<int:user_id>", "get_user", self.get_user, methods=["GET"])
        self.app.add_url_rule("/users", "create_user", self.create_user, methods=["POST"])
        self.app.add_url_rule("/users/<int:user_id>", "edit_user", self.edit_user, methods=["PUT"])
        self.app.add_url_rule("/users/<int:user_id>", "delete_user", self.delete_user, methods=["DELETE"])
        self.app.add_url_rule('/register', 'register', self.register, methods=['POST'])
        self.app.add_url_rule('/login', 'login', self.login, methods=['POST'])
        self.app.add_url_rule('/logout', 'logout', self.logout, methods=['POST'])

        self.swagger = Swagger(self.app)

    def run(self, host='0.0.0.0', port=5000):
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
        return 'pong', 200

    def get_all_users(self):
        """
        Get all users
        ---
        responses:
            200:
                description: List of all users
            500:
                description: Error occurred while retrieving users
        """
        try:
            users = self.user_service_logic.get_all_user()
            return jsonify(users), 200
        except Exception as e:
            logging.error(f"Error getting all users: {e}")
            abort(500, description="Internal Server Error. Failed to retrieve users.")

    def get_user(self, user_id):
        """
        Get user by id
        ---
        parameters:
            - name: user_id
              in: path
              type: integer
              required: true
        responses:
            200:
                description: Returns the user with given id
            404:
                description: User not found
            500:
                description: Error occurred while retrieving user
        """
        try:
            user = self.user_service_logic.get_user(user_id)
            if user:
                return jsonify(user), 200
            else:
                return jsonify({"error": "User not found"}), 404
        except Exception as e:
            logging.error(f"Error getting user: {e}")
            abort(500, description="Internal Server Error. Failed to retrieve user.")

    def create_user(self):
        """
        Create a new user
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
            201:
                description: User created successfully
            400:
                description: Invalid request, username and password required
            500:
                description: Error occurred while creating user
        """
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"error": "Invalid request, username and password required"}), 400
        try:
            self.user_service_logic.create_user(data['username'], data['password'])
            return jsonify({"message": "User created successfully"}), 201
        except Exception as e:
            logging.error(f"Error creating user: {e}")
            abort(500, description="Internal Server Error. Failed to create user.")

    def edit_user(self, user_id):
        """
        Edit a user
        ---
        parameters:
            - name: user_id
              in: path
              type: integer
              required: true
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
                description: User updated successfully
            400:
                description: Invalid request, username and password required
            500:
                description: Error occurred while updating user
        """
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"error": "Invalid request, username and password required"}), 400
        try:
            self.user_service_logic.edit_user(user_id, data['username'], data['password'])
            return jsonify({"message": "User updated successfully"}), 200
        except Exception as e:
            logging.error(f"Error updating user: {e}")
            abort(500, description="Internal Server Error. Failed to update user.")

    def delete_user(self, user_id):
        """
        Delete a user
        ---
        parameters:
            - name: user_id
              in: path
              type: integer
              required: true
        responses:
            200:
                description: User deleted successfully
            500:
                description: Error occurred while deleting user
        """
        try:
            self.user_service_logic.delete_user(user_id)
            return jsonify({"message": "User deleted successfully"}), 200
        except Exception as e:
            logging.error(f"Error deleting user: {e}")
            abort(500, description="Internal Server Error. Failed to delete user.")

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
                description: Missing username or password parameter
            404:
                description: User not found
            500:
                description: Error occurred while registering user
        """
        try:
            if not request.is_json:
                return jsonify({"msg": "Missing JSON in request"}), 400
    
            username = request.json.get('username', None)
            password = request.json.get('password', None)
    
            if not username:
                return jsonify({"msg": "Missing username parameter"}), 400
            if not password:
                return jsonify({"msg": "Missing password parameter"}), 400
    
            user = self.user_service_logic.get_user_by_username(username)
            logging.error(user['id'])
            if not user:
                return jsonify({"msg": "User not found"}), 404
    
            hashed_password = generate_password_hash(str(password), method='sha256')
    
            self.user_service_logic.edit_user(user['id'], username, hashed_password)
            return jsonify({"msg": "User registered successfully"}), 200
        except Exception as e:
            logging.error(f"Error registering user: {e}")
            abort(500)

    def login(self):
        """
        Login a user
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
                description: Successfully logged in
            400:
                description: Missing username or password parameter
            401:
                description: Bad username or password
            500:
                description: Error occurred while logging in
        """
        try:
            if not request.is_json:
                return jsonify({"msg": "Missing JSON in request"}), 400
    
            username = request.json.get('username', None)
            password = request.json.get('password', None)
    
            if not username:
                return jsonify({"msg": "Missing username parameter"}), 400
            if not password:
                return jsonify({"msg": "Missing password parameter"}), 400
    
            user = self.user_service_logic.get_user_by_username(username)
            logging.error(user)
            if user and len(user) > 0 and check_password_hash(user['password'], str(password)):
                access_token = create_access_token(identity=username)
                return jsonify(access_token=access_token), 200
            else:
                return jsonify({"msg": "Bad username or password"}), 401
        except Exception as e:
            logging.error(f"Error logging in user: {e}")
            abort(500)

    @jwt_required()
    def logout(self):
        """
        Logout a user
        ---
        parameters:
            - name: Authorization
              in: header
              type: string
              required: true
              description: Bearer token
        responses:
            200:
                description: Successfully logged out
            401:
                description: Missing or invalid JWT token
            500:
                description: Error occurred while logging out
        """
        try:
            jti = get_jwt()["jti"]
            self.BLACKLIST.add(jti)
            return jsonify({"msg": "Successfully logged out"}), 200
        except Exception as e:
            logging.error(f"Error logging out user: {e}")
            abort(500)


if __name__ == "__main__":
    app = UserServiceApplication()
    app.run()
