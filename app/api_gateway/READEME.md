# API Gateway Flask Application
This application is an API Gateway written in Python, using the Flask framework. It acts as the single entry point into the system, responsible for forwarding requests to the appropriate services (User, Message, Vote services).

A detailed overview of the endpoints is provided in the following table.

## API Endpoints
| Route              | Method      | Description                                                       | Parameters                                                                                     |
|--------------------|-------------|-------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| `/ping`            | `GET`       | Healthcheck for the service                                       | None                                                                                           |
| `/users/<path>`    | `GET, POST, PUT, DELETE` | Forward the request to the User Service                            | Path: _string_                                                                                 |
| `/messages/<path>` | `GET, POST, PUT, DELETE` | Forward the request to the Message Service                         | Path: _string_                                                                                 |

For routes that accept a body in the request, the body needs to be JSON-encoded.

The application also includes error handlers for 400 (Bad Request), 404 (Not Found), and 500 (Internal Server Error) responses.

## Not In Scope
This application serves as a basic API Gateway. Potential features that are currently not in scope, but might be considered for future development, include:

1. Rate Limiting: The gateway could be updated to limit the number of requests a client can make within a certain timeframe.
2. Caching: The gateway could cache responses to certain requests to reduce load on the services and improve response times.
3. Load Balancing: If there are multiple instances of a service, the gateway could balance the load between these instances.
