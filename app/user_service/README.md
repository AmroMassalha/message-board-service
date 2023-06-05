UserServiceApplication
Scope

The UserServiceApplication is a service responsible for handling all user-related functionalities of the application. It includes features like:

- Registering a new user and hashing their password.
- Login and Logout functionality using JWT tokens.
- User CRUD operations.
- The 'register' feature does not create a new user if they do not exist in the system, instead, it updates the password of the existing user.
  The UserServiceApplication does not handle functionalities like:

- Authenticating or authorizing other parts of the system.
- Handling other business functionalities that are not user-related.

High-Level Design
The service is developed in Flask and incorporates the Model-View-Controller pattern. It uses JWT for user authentication. The data received from the client is processed in the controller layer (Flask routes), and the business logic is handled by the service layer (user_service_logic).

We've utilized the Factory and Abstract Factory design patterns to make our UserServiceApplication more flexible and easily maintainable:

Factory Design Pattern: In our service, we create an instance of ConcreteUserServiceLogic. This serves as our 'factory' for creating user service logic. This approach abstracts the complexities involved in the creation of the object and provides a simple interface for creation. This provides us the flexibility to easily replace or change our user service logic implementation without changing the classes that use it.

Abstract Factory Design Pattern: The ConcreteUserServiceLogic can be seen as an abstract factory, with methods to create a range of related objects (like create_user, edit_user, etc). This design allows for high-level abstraction of how these objects are created, used, and interact with each other.

Abstract and Factory Design Patterns
Abstract Design Pattern provides a way to encapsulate a group of individual factories that have a common theme without specifying their concrete classes. In our case, the theme is operations related to users.

Factory Design Pattern is a creational pattern that provides an interface for creating objects in a superclass but allows subclasses to alter the type of objects that will be created. This pattern helps to create a loosely coupled system by separating the object creation and object usage parts. In our system, we have ConcreteUserServiceLogic as a factory for creating user service logic.
