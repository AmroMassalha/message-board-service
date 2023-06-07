# User Service Flask Application
This application is a User Service written in Python, using the Flask framework. It manages users in the system, providing a variety of endpoints to create, edit, retrieve, delete, register, login and logout users.

This service uses a concrete implementation of user service logic, `ConcreteUserServiceLogic`, to handle the business logic of user management.

The application uses JWT (JSON Web Tokens) for authentication. The `JWTManager` class handles the generation and verification of JWTs, which are used to authenticate user requests.

Endpoints are defined in the `UserServiceApplication` class, and the Flask application is configured with the JWT secret key and options such as token expiration and blacklist checking.

The `UserServiceApplication` also includes a `/ping` endpoint for health checking purposes.

A detailed overview of the endpoints is provided in the following table.

## API Endpoints

| Route     | Method   | Description                | Parameters                |
| :-------- | :------- | :------------------------- | :------------------------ |
| `/ping`   | `GET` | Healthcheck for the service |  None                   |
| `/users`  | `GET` | Get a list of all users |  None                   |
| `/users/<int:user_id>` | `GET` | Get specific user details |  user_id: int                   |
| `/users` | `POST` | Create a new user	 |  	Body: _{username: string, password: string}_                   |
| `/users/<int:user_id>` | `PUT` | Edit specific user details |  user_id: int, Body: _{username: string, password: string}_                   |
| `/users/<int:user_id>` | `DELETE` | Delete a specific user |  user_id: int                   |
| `/register` | `POST` | Register a new user	 |  Body: _{username: string, password: string}_                   |
| `/login` | `POST` | Login for a user |  Body: _{username: string, password: string}_                   |
| `/logout` | `POST` | Logout a user |  Header: _{Authorization: Bearer <token>}_                   |

For routes that accept a body in the request, the body needs to be JSON-encoded. Additionally, for routes that accept user_id, the `user_id` should be replaced with a valid integer user ID.

For the `/logout` route, the `Authorization` header is required, with a valid Bearer token obtained from a successful login or register request.

This application demonstrates a clean architecture for a user management service. Its design separates concerns, abstracts business logic, and provides a clear, RESTful API for client applications.

Please refer to the code and the individual API endpoint comments for a more detailed understanding of the service.
