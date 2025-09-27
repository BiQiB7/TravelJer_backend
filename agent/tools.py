from typing import List, Dict, Any, Optional
from enum import Enum
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from ..functions.find_nearby_places import find_nearby_places
from ..functions.get_route import get_route
from ..functions.get_weather_forecast import get_daily_forecast
from ..functions.search_places import search_places
from ..functions.visualize_route_on_map import visualize_route_on_map
from ..functions.get_place_details import get_place_details

# --- Enums ---
class PlaceType(str, Enum):
    AUTOMOTIVE = "Automotive"
    BUSINESS = "Business"
    CULTURE = "Culture"
    EDUCATION = "Education"
    ENTERTAINMENT_AND_RECREATION = "Entertainment and Recreation"
    FINANCE = "Finance"
    FOOD_AND_DRINK = "Food and Drink"
    GEOGRAPHICAL_AREAS = "Geographical Areas"
    GOVERNMENT = "Government"
    HEALTH_AND_WELLNESS = "Health and Wellness"
    LODGING = "Lodging"
    PLACES_OF_WORSHIP = "Places of Worship"
    SERVICES = "Services"
    SHOPPING = "Shopping"
    SPORTS = "Sports"
    TRANSPORTATION = "Transportation"

class TravelMode(str, Enum):
    WALK = "WALK"
    BICYCLE = "BICYCLE"
    TWO_WHEELER = "TWO_WHEELER"
    DRIVE = "DRIVE"
    TRANSIT = "TRANSIT"

# --- Tool Schemas ---

class FindNearbyPlacesSchema(BaseModel):
    latitude: float = Field(..., description="The latitude of the center of the search area.")
    longitude: float = Field(..., description="The longitude of the center of the search area.")
    radius: float = Field(..., description="The radius of the search area in meters.")
    included_types: Optional[List[PlaceType]] = Field(None, description="A list of place types to search for.")
    excluded_types: Optional[List[PlaceType]] = Field(None, description="A list of place types to exclude from the search.")
    max_result_count: Optional[int] = Field(None, description="The maximum number of results to return.")
    rank_preference: Optional[str] = Field(None, description="The ranking preference for the results. Can be 'POPULARITY' or 'DISTANCE'.")

class GetDailyForecastSchema(BaseModel):
    latitude: float = Field(..., description="The latitude of the location.")
    longitude: float = Field(..., description="The longitude of the location.")
    days: Optional[int] = Field(None, description="The number of forecast days to return (1-10).")

class SearchPlacesSchema(BaseModel):
    text_query: str = Field(..., description="The text string to search for (e.g., 'restaurants in San Francisco').")
    language_code: Optional[str] = Field(None, description="The language in which to return results (e.g., 'en-US').")
    max_result_count: Optional[int] = Field(None, description="The maximum number of results to return.")
    region_code: Optional[str] = Field(None, description="The region code to bias the search results (e.g., 'US').")

class ProposeDraftPlanSchema(BaseModel):
    stops: List[Dict[str, str]] = Field(..., description="A list of dictionaries, where each dictionary has 'place_id' and 'comment'.")
    travel_mode: TravelMode = Field(TravelMode.DRIVE, description="The mode of travel for the route.")

class GetPlaceDetailsSchema(BaseModel):
    place_id: str = Field(..., description="The Place ID of the place to fetch details for.")

class MessageUserSchema(BaseModel):
    message: str = Field(..., description="The message to be sent to the user.")

# --- Tool Functions ---

def _simplify_search_places_response(response_json: Dict[str, Any]) -> Dict[str, Any]:
    """Simplifies the JSON response from the search_places function."""
    simplified_places = []
    if 'places' not in response_json:
        return {"places": []}

    for place in response_json.get('places', []):
        simplified_place = {
            "id": place.get("id"),
            "displayName": place.get("displayName", {}).get("text"),
            "types": place.get("types", [])[:2],  # Keep it short
            "location": place.get("location"),
            "rating": place.get("rating"),
            "userRatingCount": place.get("userRatingCount"),
            "openNow": None,
            "openingHours": "Not available",
            "priceRange": "Not available"
        }

        if "regularOpeningHours" in place and place["regularOpeningHours"]:
            simplified_place["openNow"] = place["regularOpeningHours"].get("openNow")
            
            if "weekdayDescriptions" in place["regularOpeningHours"]:
                hours_dict = {}
                for desc in place["regularOpeningHours"]["weekdayDescriptions"]:
                    day, _, hours = desc.partition(': ')
                    if hours in hours_dict:
                        hours_dict[hours].append(day)
                    else:
                        hours_dict[hours] = [day]
                
                condensed_hours = []
                for hours, days in hours_dict.items():
                    if len(days) == 7:
                        condensed_hours.append(f"Mon-Sun: {hours}")
                        break
                    
                    day_str = ", ".join(days)
                    condensed_hours.append(f"{day_str}: {hours}")

                simplified_place["openingHours"] = "; ".join(condensed_hours)

        if "priceRange" in place and place.get("priceRange"):
            start_price = place["priceRange"].get("startPrice", {})
            end_price = place["priceRange"].get("endPrice", {})
            currency = start_price.get("currencyCode", "")
            start_units = start_price.get("units", "N/A")
            end_units = end_price.get("units", "N/A")
            simplified_place["priceRange"] = f"{currency} {start_units}-{end_units}"

        simplified_places.append(simplified_place)

    return {"places": simplified_places}


def search_places_simplified(
    text_query: str,
    language_code: Optional[str] = None,
    max_result_count: Optional[int] = None,
    region_code: Optional[str] = None
) -> Dict[str, Any]:
    """
    Searches for places based on a text query and returns a simplified response.
    """
    response = search_places(text_query, language_code, max_result_count, region_code)
    return _simplify_search_places_response(response)


def propose_draft_plan(stops: List[Dict[str, str]], travel_mode: str = 'DRIVE') -> Dict[str, Any]:
    """
    Proposes a new itinerary as a draft, complete with a route and map visualization.
    This tool should be used when the user asks for a change to the plan.
    """
    if len(stops) < 2:
        raise ValueError("At least two stops are required to create a route.")

    place_ids = [stop["place_id"] for stop in stops]
    origin_place_id = place_ids[0]
    destination_place_id = place_ids[-1]
    waypoint_place_ids = place_ids[1:-1]

    try:
        route_data = get_route(origin_place_id, destination_place_id, waypoint_place_ids, travel_mode)
        encoded_polyline = route_data["routes"][0]["polyline"]["encodedPolyline"]
        
        map_data = visualize_route_on_map(encoded_polyline, origin_place_id, destination_place_id, waypoint_place_ids)
        
        draft_itinerary = {
            "stops": stops,
            "map_data": map_data
        }
        
        
        # In a real app, this would be saved to the DB. Here, we return it
        # so the API layer can handle the state change.
        return {"agent_action":"draft_itinerary","content":draft_itinerary}

    except Exception as e:
        return {"error": f"Failed to create draft plan: {e}"}


# def confirm_draft_plan() -> Dict[str, str]:
#     """
#     Confirms the current draft plan, making it the official itinerary.
#     This tool should be used when the user agrees with the proposed draft.
#     """
#     # This tool doesn't need to do anything but signal success to the agent.
#     # The API layer will handle the state change.
#     return {"agent_action": "confirm_plan"}


def message_user(message: str) -> str:
    """
    Sends a text message to the user.
    Use this when you only need to communicate information without performing any other action.
    """
    return {"agent_action":"message","content":message}

# --- Toolsets ---

planner_tools = [
    StructuredTool.from_function(
        func=find_nearby_places,
        name="find_nearby_places",
        description="Searches for places of specific types within a given area.",
        args_schema=FindNearbyPlacesSchema,
        handle_validation_error=True,
        handle_tool_error=True
    ),
    StructuredTool.from_function(
        func=get_daily_forecast,
        name="get_daily_forecast",
        description="Retrieves the daily weather forecast for a specific location.",
        args_schema=GetDailyForecastSchema,
        handle_validation_error=True,
        handle_tool_error=True
    ),
    StructuredTool.from_function(
        func=search_places_simplified,
        name="search_places",
        description="Searches for places based on a text query.",
        args_schema=SearchPlacesSchema,
        handle_validation_error=True,
        handle_tool_error=True
    ),
    StructuredTool.from_function(
        func=propose_draft_plan,
        name="propose_draft_plan",
        description="Proposes a new itinerary with a route and map as a draft for the user to confirm.",
        args_schema=ProposeDraftPlanSchema,
        handle_validation_error=True,
        handle_tool_error=True
    ),
    StructuredTool.from_function(
        func=get_place_details,
        name="get_place_details",
        description="Fetches detailed information for a specific place using its Place ID.",
        args_schema=GetPlaceDetailsSchema,
        handle_validation_error=True,
        handle_tool_error=True
    ),
    # StructuredTool.from_function(
    #     func=confirm_draft_plan,
    #     name="confirm_draft_plan",
    #     description="Confirms the current draft plan, making it the official itinerary.",
    #     handle_validation_error=True,
    #     handle_tool_error=True
    # ),
    StructuredTool.from_function(
        func=message_user,
        name="message_user",
        description="Sends a text message to the user.",
        args_schema=MessageUserSchema,
        handle_validation_error=True,
        handle_tool_error=True
    ),

    #
]
kawan_tools=planner_tools
# kawan_tools = planner_tools + [
#     StructuredTool.from_function(
#         func=propose_draft_plan,
#         name="propose_draft_plan",
#         description="Proposes a new itinerary with a route and map as a draft for the user to confirm.",
#         args_schema=ProposeDraftPlanSchema,
#     ),
# ]