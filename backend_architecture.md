# City Weaver AI - Backend Architecture (v4)

This document outlines the backend architecture for the City Weaver AI, focusing on a modular, agent-based approach to handle travel planning and user interaction.

## Directory Structure

The backend will be organized into the following directory structure to ensure a clear separation of concerns:

```
city_weaver_ai/
├── agent/
│   ├── __init__.py
│   ├── agent.py      # Core agent logic (using LangChain)
│   ├── prompts.py    # Prompts for persona generation
│   └── tools.py      # Tools for the agents
├── api/
│   ├── __init__.py
│   ├── main.py       # FastAPI application and endpoints
│   └── schemas.py    # Pydantic schemas for API validation
├── core/
│   ├── __init__.py
│   └── security.py   # Authentication and security helpers
├── llm/
│   ├── __init__.py
│   ├── base.py       # Base class for LLM models
│   ├── chat.py       # Chat manager for conversation history
│   └── google_chat.py # Google GenAI implementation
├── functions/
│   ├── ...           # Existing Python functions for external APIs
└── requirements.txt
```

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

## Data Flow Diagram

```mermaid
graph TD
    A[User] -->|HTTP Request| B(api/main.py);
    B --> C{Authentication};
    C -->|Authenticated| D(Persona & Plan Management);
    D -->|Generate Persona| I(llm/google_chat.py);
    D -->|Create/Update Plan| E(agent/agent.py);
    E -->|Use Tools| F(agent/tools.py);
    F -->|Call Functions| G(functions/*.py);
    G -->|External APIs| H(Google Maps, Weather, etc.);
    H --> G;
    G --> F;
    F --> E;
    E -->|LLM Call| I(llm/google_chat.py);
    I -->|Gemini API| J[Google GenAI];
    J --> I;
    I --> E;
    E --> D;
    D -->|Save to DB| K[(In-Memory DB)];
    D -->|HTTP Response| A;