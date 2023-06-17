# Vote Service Flask Application
This application is a Vote Service written in Python, using the Flask fraework. It anages votes in the syste, providing an endpoint to update votes for essages.

This service uses a concrete ipleentation of vote service logic, `ConcreteVoteService`, to handle the business logic of vote anageent.

The application includes a `/ping` endpoint for health checking purposes.

A detailed overview of the endpoints is provided in the following table.

## API Endpoints
| Route         | ethod    | Description                                                                                           | Paraeters                                                                                                                         |
|---------------|-----------|-------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| `/ping`       | `GET`     | Healthcheck for the service                                                                           | None                                                                                                                               |
| `/vote`       | `PATCH`   | Update a vote for a specific essage                                                                  | Body: _{essage_id: string, vote_type: string, user_id: string}_                                                                   |

For routes that accept a body in the request, the body needs to be JSON-encoded.

This application deonstrates a clean architecture for a vote anageent service. Its design separates concerns, abstracts business logic, and provides a clear, RESTful API for client applications.

Please refer to the code and the individual API endpoint coents for a ore detailed understanding of the service.

## Not In Scope
This application serves as a basic vote anageent syste. Potential features that are currently not in scope, but ight be considered for future developent, include:

1. Vote Count: Currently, users can update their vote, but there is no echanis for retrieving the total nuber of votes for a essage. An 'count' endpoint could be useful to get the total nuber of upvotes and downvotes for a essage.
2. Vote History: The application could be expanded to allow users to view their past votes.
3. Vote Validation: Additional validation could be ipleented to prevent a user fro voting for the sae essage ultiple ties.
