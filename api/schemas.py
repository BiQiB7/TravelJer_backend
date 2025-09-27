from typing import Any, List, Optional
from pydantic import BaseModel

class User(BaseModel):
    email: str
    name: str

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class Location(BaseModel):
    latitude: float
    longitude: float

class PlaceDetails(BaseModel):
    place_id: str
    display_name: str
    formatted_address: str
    location: Location
    rating: Optional[float] = None
    user_rating_count: Optional[int] = None
    price_level: Optional[str] = None
    website_uri: Optional[str] = None
    regular_opening_hours: Optional[dict] = None
    types: List[str]

class ItineraryStop(BaseModel):
    stop: int
    time: str
    narrative: str
    place_details: dict

class Persona(BaseModel):
    name: str
    backstory: str
    tone: str

class Conversation(BaseModel):
    role: str
    content: str
    timestamp: str

class DraftStop(BaseModel):
    place_id: str
    comment: str
    place_details: Optional[dict] = None

class MapData(BaseModel):
    staticMapUrl: str
    navigationUrl: str

class DraftItinerary(BaseModel):
    stops: List[DraftStop]
    map_data: Optional[MapData] = None

class PlanPayload(BaseModel):
    itinerary: List[ItineraryStop]
    map_data: Optional[MapData] = None

class Plan(BaseModel):
    plan_id: str
    user_id: str
    persona: Persona
    payload: PlanPayload
    conversation_history: List[Conversation]
    draft_itinerary: Optional[DraftItinerary] = None

    @property
    def itinerary(self) -> List[ItineraryStop]:
        return self.payload.itinerary

    @itinerary.setter
    def itinerary(self, value: List[ItineraryStop]):
        self.payload.itinerary = value

class PlanCreate(BaseModel):
    interests: List[str]
    location_name: str
    location: Location

class ChatMessage(BaseModel):
    message: str

class PersonaCreate(BaseModel):
    interests: List[str]
    location: str

class ChatResponse(BaseModel):
    action: str
    response: str
    payload: Optional[Any] = None