# Message Board Application - Microservices Architecture

Welcome to the microservices architecture of the Message Board Application. This guide will give you an overview of the structure of each microservice, configuration management, database initialization, containerization, the foundation directory, and the setup process.

## Microservice Structure
Each microservice in the Message Board Application is built on the following architecture:

* ***Abstract Python Class***: Each microservice begins with an abstract base class. This class provides a set of interfaces that are intended to be fully implemented in the concrete class.

* ***Concrete Python Class***: The concrete class inherits from the abstract base class and provides implementations for the interfaces defined in the abstract class.

* ***Flask App***: On top of the concrete class, we have the Flask app itself which handles all the routing and server-side logic of the microservice.

    ### Configuration Management
    Each microservice contains a config directory which includes different `JSON` files for configuration. These JSON files provide an easy and     flat flow for managing different configurations for each service.

    ### Database Initialization
    Each microservice contains an `init.sql` script file. These scripts describe the structure of the database table(s) specific to each microservice.

    ### Containerization
    Each microservice includes a `Dockerfile` that enables it to be containerized. This allows each microservice to be deployed and run in a consistent environment.

    In addition to the microservice-specific Dockerfiles, the main directory includes a `MySQL` Dockerfile that copies `init.sql` scripts from each microservice.

## Docker Compose
The main directory contains a Docker Compose file. This file includes the definitions of all services making up the Message Board Application, allowing them to be built, started, and stopped together.

## Foundation Directory
The foundation directory is an essential component of the application. It contains the following:

* ***Singletons***: These are classes that restrict the instantiation of a class to a single instance, ensuring that a class has only one instance, and provides a global point of access to it.
* ***Token Management***: This component handles token creation and validation. It's vital for maintaining secure user sessions and API authorization.
* ***Database Client***: This is a custom wrapper around our database interactions. It provides a unified interface for the various microservices to interact with the database.
* ***Configuration Reader***: This utility reads and validates configuration files for the microservices.

## Python Requirements
The `requirements.txt` file in the main directory lists all Python packages required by the application.

## Setup Script
The `setup.sh` script in the main directory prepares the local machine to run the application using Docker.

# Setup Steps
1. **Clone the repository**: Clone the Message Board application repository to your local machine.

2. **Run setup.sh**: Navigate to the cloned repository and run the setup script. This script is designed to detect your operating system and install the necessary dependencies.
```bash
./setup.sh
```
The script will perform the _following tasks_:

* Verify Python version: Checks if Python 3.10 or higher is installed. If not, it will offer to install it.
* Install Docker: If Docker is not installed, it will offer to install it.
* Install Docker Compose: If Docker Compose is not installed, it will offer to install it.
* Create and activate a virtual environment: The script will set up a Python virtual environment for the application and activate it.
* Install requirements: The script will install the required Python packages listed in the requirements.txt file.
* Install pre-commit hooks: The script will install the pre-commit hooks for the application.
* Build and run Docker Compose: Finally, the script will use Docker Compose to build and run the application.


--------------------------------------------------------------------------------------


We invite you to explore, use, and contribute to this project. Don't hesitate to reach out if you encounter any issues or have suggestions.

# Support
Our supportive and energetic team is always on standby to assist you. Reach out to us via email at amr.massalha@gmail.com, or join our vibrant Slack channel. Your journey with our Message Board Application is as much our journey, and we are committed to making it a successful and enjoyable one.
