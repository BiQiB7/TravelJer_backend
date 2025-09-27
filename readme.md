# City Weaver AI - API Architecture (v4)

This document outlines the API endpoints and data schemas for the City Weaver AI frontend, updated to include user authentication and data persistence.

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