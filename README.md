
# Message Board Microservices

### Overview
The Message Board Microservices project consists of multiple decoupled services including User Service, Message Service, Vote Service, and API Gateway. Each service is dedicated to a specific functionality offering granular control and simplifying the overall management of the message board.

The main motivation behind this project is to provide a simplified way for clients to manage messages, including creating, voting, updating, and deleting them, all while ensuring a high level of security.

By leveraging the power of microservices architecture, each component can be developed, deployed, and scaled independently. This provides great flexibility and helps in faster feature releases, easier maintenance, and efficient scaling based on individual service load.
### Architecture
The project follows the microservices architectural style. It is composed of:

1. ***User Service***: Manages all operations related to users. It provides functionality for user registration, authentication, and profile management. Each user is associated with a unique identifier which is used across other services. The service also ensures the security of user data by implementing appropriate encryption techniques and secure access policies. This service communicates with others using its API and uses MySQL as its database system.

2. ***Message Service***: Handles message-related operations. Each message is associated with a user identifier and a unique message identifier. This service supports operations like posting a new message, updating an existing message, and deleting a message. All messages are timestamped, and access to modify or delete messages is controlled based on the user. The Message Service communicates with the User and Vote services through their APIs and uses MySQL for its database needs.

3. ***Vote Service***: Manages voting operations for the messages. It allows users to upvote or downvote messages. Each vote is associated with a user identifier and a message identifier, ensuring that a user can vote only once for a specific message. The service also provides functionality to fetch the current vote count for a message. This service communicates with the Message Service using its API and uses MySQL for data persistence.

4. ***API Gateway***: Serves as the single entry point for all clients. It routes requests to the appropriate microservices and aggregates the responses. The gateway also implements rate limiting and access control policies to protect the services from abusive access patterns. It performs protocol translation, request routing, load balancing, and can provide API analytics and logging.

All these services communicate with each other using synchronous HTTP/REST protocols. They each have their own MySQL databases to ensure loose coupling and service independence.

The architecture is designed to be resilient, distributed, and scalable. We use containerization (with Docker) and orchestration tools (like Kubernetes) to deploy and manage the microservices.

Please refer to individual service documentation for more detailed architecture and design choices.

### Prerequisites
1. Operating System: Linux or MacOS
2. `Python`: Version 3.10 or higher
3. `Docker`: For containerizing the application
4. `Docker Compose`: For defining and running multi-container Docker applications
Note: If these prerequisites are not met, the setup script will attempt to install the necessary dependencies. Please ensure you have a stable internet connection for this process.

#### Further Setup
Please navigate to the `./app` directory and refer to the README file present for more detailed information about the application's structure and how to interact with it.


As for the `./terraform` and `./helm` directories, please note that their respective documentations are currently TBD (To Be Determined). Check back later for updates.
