import json
import logging
import uuid
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException

from ..agent.agent import KawanAgent, PlannerAgent
from ..agent.prompts import PERSONA_GENERATION_PROMPT
from ..agent.tools import kawan_tools, planner_tools
from ..functions.find_nearby_places import find_nearby_places
from ..functions.get_place_details import get_place_details
from ..functions.get_public_transport_data import get_gtfs_realtime_data, get_gtfs_static_data
from ..functions.get_route import get_route
from ..functions.get_weather_forecast import get_daily_forecast
from ..functions.search_places import search_places
from ..functions.search_reddit import search_reddit_for_links
from ..functions.visualize_route_on_map import visualize_route_on_map
from ..core.utils import extract_json_from_string
from ..llm.chat import ChatManager
from ..llm.google_chat import GoogleGenAIChatModel
from .schemas import (ChatMessage, ChatResponse, Conversation, DraftItinerary,
                      DraftStop, ItineraryStop, Location, Plan, PlanCreate,
                      Persona, PersonaCreate, PlaceDetails, PlanPayload)
from flask_cors import CORS
from fastapi.middleware.cors import CORSMiddleware
# --- FastAPI App Initialization ---
app = FastAPI()
origins = ["*"] # "http://localhost:3000/"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


  # If using FastAPI
  
# --- In-memory "Database" ---
db_plans = {}
chat_managers: Dict[str, ChatManager] = {}

# --- Logging Setup ---
logging.basicConfig(
    filename='api_errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
 
# --- Helper Functions ---
def _process_itinerary_data(itinerary_data: Dict) -> List[ItineraryStop]:
    """Parses itinerary data, fetches place details, and returns a list of ItineraryStop objects."""
    if not itinerary_data or "stops" not in itinerary_data:
        raise HTTPException(status_code=500, detail="Processed data is missing 'stops'.")

    try:
        itinerary = []
        for i, stop_data in enumerate(itinerary_data["stops"]):
            place_id = stop_data.get("place_id")
            if not place_id:
                logging.warning(f"Stop {i+1} is missing a place_id.")
                continue

            # Fetch full place details
            place_details = get_place_details(place_id)
            if not place_details:
                continue  # Or handle the error appropriately

            itinerary.append(ItineraryStop(
                stop=i + 1,
                time="N/A",  # Placeholder for time
                narrative=stop_data.get("comment", ""),
                place_details=place_details
            ))
        return itinerary
    except (TypeError, KeyError) as e:
        raise HTTPException(status_code=500, detail=f"Agent returned malformed stop data: {e}")


def _process_draft_itinerary(draft_data: Dict) -> DraftItinerary:
    """Parses draft itinerary data, fetches place details for each stop, and returns a DraftItinerary object."""
    if not draft_data or "stops" not in draft_data:
        raise HTTPException(status_code=500, detail="Draft data is missing 'stops'.")

    try:
        enriched_stops = []
        for stop_data in draft_data["stops"]:
            place_id = stop_data.get("place_id")
            if not place_id:
                continue

            place_details = get_place_details(place_id)
            if not place_details:
                continue
            
            # Create a new dictionary with all original keys plus the new one
            enriched_stop_data = {**stop_data, "place_details": place_details}
            enriched_stops.append(DraftStop(**enriched_stop_data))

        # Create the final DraftItinerary object
        return DraftItinerary(stops=enriched_stops, map_data=draft_data.get("map_data"))

    except (TypeError, KeyError) as e:
        raise HTTPException(status_code=500, detail=f"Agent returned malformed draft stop data: {e}")


# --- API Endpoints ---
 
@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


@app.post("/api/personas", response_model=Persona)
async def create_persona(persona_data: PersonaCreate):
    try:
        model = GoogleGenAIChatModel(model_name='gemini-2.5-flash')
        prompt = PERSONA_GENERATION_PROMPT.format(
            interests=", ".join(persona_data.interests),
            location=persona_data.location
        )
        
        response, _, _ = model.send_message([prompt])
        
        if not response:
            raise ValueError("LLM returned an empty response.")

        persona_json = extract_json_from_string(response)
        return Persona(**persona_json)
    except Exception as e:
        logging.error(f"An error occurred in create_persona: {e}", exc_info=True)
        # Catch any error from model initialization, API call, or parsing
        # and return a proper JSON error response.
        raise HTTPException(status_code=500, detail=f"Failed to generate persona: {e}")

@app.post("/api/plans", response_model=Plan)
async def create_plan(plan_data: PlanCreate):
    plan_id = str(uuid.uuid4())

    # --- Persona Generation ---
    try:
        # Create a PersonaCreate object from the plan_data
        persona_create_data = PersonaCreate(
            interests=plan_data.interests,
            location=plan_data.location_name
        )
        print(persona_create_data)
        # Call the existing create_persona function to generate the persona
        persona = await create_persona(persona_create_data)
        print(persona)
    except HTTPException as e:
        # Propagate HTTP exceptions from persona creation
        raise e
    except Exception as e:
        # Catch any other unexpected errors during persona creation
        logging.error(f"An error occurred during persona creation step in create_plan: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate persona during plan creation: {e}")

    # --- Plan Generation ---
    agent = PlannerAgent(tools=planner_tools)

    system_prompt = f"""
    You are {persona.name}, a {persona.tone} tour guide.
    Your backstory: {persona.backstory}
    You are planning a tour for a user near latitude {plan_data.location.latitude} and longitude {plan_data.location.longitude}.
    Your task is to create a 2-3 stop itinerary.
    Use your available tools to find interesting places.
    Finally return your itinerary plan JSON through the `propose_draft_plan` tool.
    """

    human_prompt = "Please create a travel plan for me."

    # The agent's run method is a generator, so we iterate to get the final result
    agent_response = None
    agent_response = agent.run(human_prompt, system_prompt)
    logging.info(f"Agent response: {agent_response}")

    if not agent_response:
        raise HTTPException(status_code=500, detail="Agent failed to generate a plan.")

    # The agent's response is now expected to be a dictionary
    # with the plan details nested under the 'content' key.
    if not isinstance(agent_response, dict) or "content" not in agent_response:
        raise HTTPException(status_code=500, detail="Agent returned an invalid response format.")

    itinerary_data = agent_response["content"]
    itinerary = _process_itinerary_data(itinerary_data)

    # Create a payload object
    plan_payload = PlanPayload(
        itinerary=itinerary,
        map_data=itinerary_data.get("map_data")  # Assuming map_data might be in the agent's response
    )

    new_plan = Plan(
        plan_id=plan_id,
        user_id="default_user",  # Placeholder user_id
        persona=persona,
        payload=plan_payload,
        conversation_history=[]
    )

    db_plans[plan_id] = new_plan

    # Initialize a persistent Kawan agent for this plan
    kawan_agent = KawanAgent(tools=kawan_tools, plan=new_plan)
    chat_managers[plan_id] = kawan_agent

    return new_plan

@app.get("/api/plans", response_model=List[Plan])
async def get_plans():
    return list(db_plans.values())

@app.get("/api/plans/{plan_id}", response_model=Plan)
async def get_plan(plan_id: str):
    plan = db_plans.get(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan

@app.post("/api/plans/{plan_id}/chat", response_model=ChatResponse)
async def chat_with_plan(plan_id: str, message: ChatMessage):
    plan = db_plans.get(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    chat_manager = chat_managers.get(plan_id)
    if not chat_manager:
        raise HTTPException(status_code=500, detail="Chat manager not found for this plan")

    # Save user message to history BEFORE agent runs
    plan.conversation_history.append(Conversation(role="user", content=message.message, timestamp="..."))

    agent_response = chat_manager.run(message.message)

    if not agent_response:
        raise HTTPException(status_code=500, detail="Agent failed to generate a response.")

    action = agent_response.get("action")
    payload = agent_response.get("payload")
    raw_message = agent_response.get("message")

    # Normalize the response message
    if isinstance(raw_message, dict) and "content" in raw_message:
        response_message = raw_message["content"]
    elif isinstance(raw_message, str):
        response_message = raw_message
    else:
        # Fallback for unexpected message formats
        response_message = str(raw_message)

    if action == "error":
        raise HTTPException(status_code=500, detail=payload.get("error_message", "Unknown agent error"))

    # Save agent's response to history
    plan.conversation_history.append(Conversation(role="assistant", content=response_message, timestamp="..."))

    response_payload = None
    if action == "propose_draft_plan":
        try:
            # The payload should directly contain the draft itinerary content
            if not isinstance(payload, dict) or "content" not in payload:
                raise HTTPException(status_code=500, detail="KawanAgent returned an invalid plan format.")
            
            itinerary_data = payload["content"]
            
            # Process the draft itinerary to include place details
            # Process the draft itinerary to include place details
            processed_draft = _process_draft_itinerary(itinerary_data)
            
            plan.draft_itinerary = processed_draft

            # Convert DraftItinerary to the desired response format for the payload
            response_itinerary = []
            if processed_draft and processed_draft.stops:
                for i, draft_stop in enumerate(processed_draft.stops):
                    if draft_stop.place_details:
                        response_itinerary.append(ItineraryStop(
                            stop=i + 1,
                            time="N/A",  # Placeholder for time
                            narrative=draft_stop.comment,
                            place_details=draft_stop.place_details
                        ))

            response_payload = {
                "itinerary": response_itinerary,
                "map_data": processed_draft.map_data if processed_draft else None
            }

        except HTTPException as e:
            # Re-raise HTTP exceptions from the helper
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to parse and save draft itinerary: {e}")

    elif action == "confirm_plan":
        # This action is currently not used by the agent but is kept for future use.
        # The confirmation logic is handled by the /confirm endpoint.
        pass

    # For all actions ('message_user', 'propose_draft_plan', 'confirm_plan'),
    # return the updated plan and the agent's conversational message.
    return ChatResponse(action=action, response=response_message, payload=response_payload)


@app.post("/api/plans/{plan_id}/confirm", response_model=Plan)
async def confirm_plan_changes(plan_id: str):
    plan = db_plans.get(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    if not plan.draft_itinerary:
        raise HTTPException(status_code=400, detail="No draft itinerary to confirm.")
        
    # Convert DraftItinerary to a new PlanPayload
    new_itinerary_stops = []
    if plan.draft_itinerary and plan.draft_itinerary.stops:
        for i, draft_stop in enumerate(plan.draft_itinerary.stops):
            if draft_stop.place_details:
                new_itinerary_stops.append(ItineraryStop(
                    stop=i + 1,
                    time="N/A",  # Placeholder for time
                    narrative=draft_stop.comment,
                    place_details=draft_stop.place_details
                ))

    # Create a new payload for the plan
    plan.payload = PlanPayload(
        itinerary=new_itinerary_stops,
        map_data=plan.draft_itinerary.map_data if plan.draft_itinerary else None
    )
    plan.draft_itinerary = None
    
    return plan


@app.post("/api/functions/find_nearby_places")
async def find_nearby_places_endpoint(latitude: float, longitude: float, radius: float, included_types: Optional[List[str]] = None, excluded_types: Optional[List[str]] = None, max_result_count: Optional[int] = None, rank_preference: Optional[str] = None):
    return find_nearby_places(latitude, longitude, radius, included_types, excluded_types, max_result_count, rank_preference)

@app.post("/api/functions/get_place_details")
async def get_place_details_endpoint(place_id: str):
    return get_place_details(place_id)

@app.post("/api/functions/get_public_transport_data/realtime")
async def get_gtfs_realtime_data_endpoint(agency: str, category: Optional[str] = None):
    return get_gtfs_realtime_data(agency, category)

@app.post("/api/functions/get_public_transport_data/static")
async def get_gtfs_static_data_endpoint(agency: str, category: Optional[str] = None):
    return get_gtfs_static_data(agency, category)

@app.post("/api/functions/get_route")
async def get_route_endpoint(origin_place_id: str, destination_place_id: str, waypoint_place_ids: Optional[List[str]] = None, travel_mode: Optional[str] = None):
    return get_route(origin_place_id, destination_place_id, waypoint_place_ids, travel_mode)

@app.post("/api/functions/get_weather_forecast")
async def get_daily_forecast_endpoint(latitude: float, longitude: float, days: Optional[int] = None):
    return get_daily_forecast(latitude, longitude, days)

@app.post("/api/functions/search_places")
async def search_places_endpoint(text_query: str, language_code: Optional[str] = None, max_result_count: Optional[int] = None, region_code: Optional[str] = None):
    return search_places(text_query, language_code, max_result_count, region_code)

@app.post("/api/functions/search_reddit")
async def search_reddit_for_links_endpoint(query: str, subreddit_limit: Optional[int] = 5, post_limit: Optional[int] = 10):
    return search_reddit_for_links(query, subreddit_limit, post_limit)

@app.post("/api/functions/visualize_route_on_map")
async def visualize_route_on_map_endpoint(encoded_polyline: str, origin_place_id: str, destination_place_id: str, waypoint_place_ids: Optional[List[str]] = None):
    return visualize_route_on_map(encoded_polyline, origin_place_id, destination_place_id, waypoint_place_ids)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)