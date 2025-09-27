# TravelJer backend architecture

This document outlines the backend architecture for the TravelJer backend architecture, focusing on a modular, agent-based approach to handle travel planning and user interaction.

## Directory Structure

The backend will be organized into the following directory structure to ensure a clear separation of concerns:

## Component Responsibilities

-   **`agent/`**: This module contains the core AI agent responsible for generating and modifying travel plans.
    -   `agent.py`: Defines the `PlannerAgent` and the `KawanAgent`.
        -   **`PlannerAgent`**: A one-shot agent responsible for creating the initial itinerary.
        -   **`KawanAgent`**: A persistent, conversational agent with memory, responsible for all user interactions after the initial plan is created.
    -   `prompts.py`: Contains the prompt templates for persona generation.
    -   `tools.py`: Defines the tools available to the agents. The `KawanAgent` will have an additional tool, `propose_draft_plan`, which is not available to the `PlannerAgent`.

-   **`api/`**: This is the main entry point for the backend, handling all HTTP requests.
    -   `main.py`: The FastAPI application, which will implement the endpoints defined in `api_architecture.md`. It will handle user authentication, plan management, and will delegate the core logic to the `agent`.
    -   `schemas.py`: Contains all the Pydantic models for request and response validation, ensuring data consistency.

-   **`core/`**: This module contains core functionalities like security and configuration.
    -   `security.py`: Manages user authentication, password hashing, and JWT creation/validation.

-   **`llm/`**: This module provides a standardized interface for interacting with different Large Language Models.
    -   The existing structure will be used to manage conversations and send requests to the Google GenAI API.

## Agent-Based Workflow

The core of the application is the AI agent, which will be responsible for creating and modifying travel plans. Here's how it will work:

1.  **Persona Generation (`POST /api/personas`)**:
    -   The user selects their interests (e.g., "food," "history").
    -   The `api/main.py` endpoint uses a prompt from `agent/prompts.py` to call the LLM and generate a persona.
    -   The generated persona is returned to the user for confirmation.

2.  **Plan Creation (`POST /api/plans`)**:
    -   The user confirms the persona and initiates plan creation.
    -   The `api/main.py` endpoint initializes a `PlannerAgent`.
    -   The agent's final output (the itinerary JSON) is taken and saved to the database.
    -   A persistent `KawanAgent` is then initialized with the persona and stored in memory, associated with the `plan_id`.

3.  **Conversational Re-planning (`POST /api/plans/{plan_id}/chat`)**:
    -   The `api/main.py` endpoint retrieves the persistent Kawan Agent for the plan.
    -   The user's message is sent to the agent. The agent's memory module provides the conversation history.
    -   The `KawanAgent` processes the input and returns a dictionary indicating the response `type` (`"text"` or `"itinerary"`) and the `data`.
    -   If the user requests a change and the agent calls the `propose_draft_plan` tool, the agent's response will be of type `"itinerary"`.
    -   The `propose_draft_plan` tool will:
        1.  Call the `get_route` function to calculate the route between the places.
        2.  Call the `visualize_route_on_map` function with the resulting polyline.
        3.  Return a dictionary containing the stops and map data.
    -   The `api/main.py` endpoint receives the agent's response.
        -   If the type is `"itinerary"`, it saves the data to the `draft_itinerary` field and adds a confirmation message to the conversation history.
        -   If the type is `"text"`, it saves the conversational response to the history.

4.  **Confirm Plan Changes (`POST /api/plans/{plan_id}/confirm`)**:
    -   The user confirms the draft plan.
    -   The `api/main.py` endpoint copies the `draft_itinerary` to the main `itinerary` and clears the draft.
    -   The updated plan is returned.


# TravelJer API Schema

This document outlines the API endpoints and data schemas for the TravelJer frontend, updated to include user authentication and data persistence.

## Authentication

- **Endpoint:** `POST /api/auth/register`
- **Description:** Creates a new user account.
- **Request Body:** `{"email": "string", "password": "string", "name": "string"}`
- **Response Body:** `{"user_id": "string", "token": "string"}`

- **Endpoint:** `POST /api/auth/login`
- **Description:** Authenticates a user and returns a JWT.
- **Request Body:** `{"email": "string", "password": "string"}`
- **Response Body:** `{"token": "string"}`

## Endpoints

### 1. Generate Persona

- **Endpoint:** `POST /api/personas`
- **Description:** Generates a persona based on user interests.
- **Request Body:** `{"interests": ["string"], "location": "string"}`
- **Response Body:**
  ```json
  {
    "name": "string",
    "backstory": "string",
    "tone": "string"
  }
  ```

### 2. Create & Manage Plans

- **Endpoint:** `POST /api/plans`
- **Description:** Creates a new travel plan for the authenticated user.
- **Request Body:** `{"persona": {"name": "string", "backstory": "string", "tone": "string"}, "location": {"latitude": "float", "longitude": "float"}}`
- **Response Body:** (Returns the full plan object, see schema below)

- **Endpoint:** `GET /api/plans`
- **Description:** Retrieves all saved travel plans for the authenticated user.
- **Response Body:** `{"plans": [{"plan_id": "string", "name": "string", "created_at": "datetime"}]}`

- **Endpoint:** `GET /api/plans/{plan_id}`
- **Description:** Retrieves a specific travel plan, including its itinerary and conversation history.
- **Response Body:** (Returns the full plan object)

### 3. Conversational Re-planning

- **Endpoint:** `POST /api/plans/{plan_id}/chat`
- **Description:** Sends a user's message to the AI for re-planning. The conversation is saved.
- **Request Body:** `{"message": "string"}`
- **Response Body:**  {"type":str, "response": Plan or str} (the agent can return a new plan, or just a text message)

### 4. Confirm Plan Changes

- **Endpoint:** `POST /api/plans/{plan_id}/confirm`
- **Description:** Confirms the draft itinerary, making it the active itinerary.
- **Response Body:** (Returns the updated plan object)

## Data Schemas

### Plan Schema
```json
{
  "plan_id": "string",
  "user_id": "string",
  "persona": {
    "name": "string",
    "backstory": "string",
    "tone": "string"
  },
  "itinerary": [
    {
      "stop": "integer",
      "time": "string",
      "narrative": "string",
      "place_details": {
        "place_id": "string",
        "display_name": "string",
        "formatted_address": "string",
        "location": { "latitude": "float", "longitude": "float" },
        "rating": "float",
        "user_rating_count": "integer",
        "price_level": "string",
        "website_uri": "string",
        "regular_opening_hours": "object",
        "types": ["string"]
      }
    }
  ],
  "conversation_history": [
    {
      "role": "enum(user|assistant)",
      "content": "string",
      "timestamp": "datetime"
    }
  ],
  "draft_itinerary": {
    "stops": [
      {
        "place_id": "string",
        "comment": "string"
      }
    ],
    "map_data": {
      "staticMapUrl": "string",
      "navigationUrl": "string"
    }
  }
}
```
## IGNORE THIS FOR NOW
## Real-Time Interaction & Notifications

To support proactive engagement (e.g., "look around, you'll see..."), the system will use push notifications. The backend will trigger these based on the user's real-time GPS location relative to the itinerary stops.

- **Mechanism:** WebSockets or a dedicated Push Notification service (e.g., Firebase Cloud Messaging).
- **Trigger:** User's device sends periodic location updates to the backend. When the user is near a point of interest, the backend sends a notification.

## Updated API Interaction Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend

    User->>Frontend: Registers/Logs In
    Frontend->>Backend: POST /api/auth/login
    Backend->>Frontend: Returns JWT

    User->>Frontend: Selects Interests
    Frontend->>Backend: POST /api/personas
    Backend->>Frontend: Returns Generated Persona
    Frontend->>User: Displays Persona, User Confirms
    User->>Frontend: Starts Plan with Persona
    Frontend->>Backend: POST /api/plans (with JWT & Persona)
    Backend->>Frontend: Returns Initial Plan
    Frontend->>User: Displays Itinerary

    User->>Frontend: Types message
    Frontend->>Backend: POST /api/plans/{plan_id}/chat (with JWT)
    Backend->>Frontend: Returns Updated Plan with Draft Itinerary
    Frontend->>User: Displays new response and draft itinerary
    User->>Frontend: Confirms changes
    Frontend->>Backend: POST /api/plans/{plan_id}/confirm
    Backend->>Frontend: Returns Confirmed Plan

    %% Background Process
    participant Device
    Device->>Backend: Sends GPS Location periodically
    Backend->>Device: Sends Push Notification (when near POI)