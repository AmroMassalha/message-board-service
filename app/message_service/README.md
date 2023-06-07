# Message Service Flask Application
This application is a Message Service written in Python, using the Flask framework. It manages messages in the system, providing a variety of endpoints to create, retrieve, delete messages, as well as vote for messages.

This service uses a concrete implementation of message service logic, `ConcreteMessageService`, to handle the business logic of message management.

The application uses JWT (JSON Web Tokens) for authentication. JWTs are used to authenticate user requests.

Endpoints are defined in the `MessageView`, `MessageVoteView`, `PingView`, and `VoteServiceHealthCheckView` classes, and the Flask application is configured with the JWT secret key.

The application also includes a `/ping` endpoint for health checking purposes.

A detailed overview of the endpoints is provided in the following table.

## API Endpoints
| Route                     | Method    | Description                                                   | Parameters                                                         |
|---------------------------|-----------|---------------------------------------------------------------|--------------------------------------------------------------------|
| `/ping`                   | `GET`     | Healthcheck for the service                                   | None                                                               |
| `/messages`               | `GET`     | Get a list of all messages                                    | None                                                               |
| `/user/messages`          | `GET`     | Get all messages from the authenticated user                  | Header: _{Authorization: Bearer <token>}_                          |
| `/messages`               | `POST`    | Post a new message                                            | Header: _{Authorization: Bearer <token>}_ Body: _{message: string}_|
| `/messages/<message_id>`  | `DELETE`  | Delete a specific message                                     | Header: _{Authorization: Bearer <token>}_ Path: _{message_id}_     |
| `/messages/<message_id>/vote` | `PUT` | Vote for a message                                            | Header: _{Authorization: Bearer <token>}_ Path: _{message_id}_ Body: _{vote_type: string}_|
| `/vote_service_health`    | `GET`     | Healthcheck for the vote service                               | None                                                               |

For routes that accept a body in the request, the body needs to be JSON-encoded. Additionally, for routes that accept a path parameter (`<message_id>`), replace it with a valid message ID.

For routes that require authentication, the `Authorization` header is required, with a valid Bearer token obtained from a successful login or register request in the User Service.

This application demonstrates a clean architecture for a message management service. Its design separates concerns, abstracts business logic, and provides a clear, RESTful API for client applications.

Please refer to the code and the individual API endpoint comments for a more detailed understanding of the service.
