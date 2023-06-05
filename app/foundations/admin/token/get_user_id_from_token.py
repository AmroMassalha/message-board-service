import logging
from functools import wraps
from flask import request, g, jsonify, current_app
from jwt import decode, InvalidTokenError

def jwt_token_required(require_user_id=False):
    """
    Decorator to decode the JWT token and optionally retrieve user id.
    If require_user_id is True, injects the user_id into the flask 'g' object.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            SECRET_KEY = current_app.config.get('SECRET_KEY')
            token = request.headers.get('Authorization')
            # TODO: implement database check token issued
            if not token:
                logging.error('Authorization token not found in headers.')
                return jsonify({"error": "Unauthorized"}), 401
            try:
                data = decode(token, SECRET_KEY, algorithms=["HS256"])
                if require_user_id:
                    user_id = data['user_id']
                    if not user_id:
                        logging.error('User ID not found in token data.')
                        return jsonify({"error": "Invalid token"}), 401
                    g.user_id = user_id
                return func(*args, **kwargs)
            except InvalidTokenError as e:
                logging.error(f'Invalid token: {e}.')
                return jsonify({"error": "Invalid token"}), 401
            except Exception as e:
                logging.error(f'Error decoding token: {e}.')
                return jsonify({"error": "Invalid token"}), 401
        return wrapper
    return decorator
