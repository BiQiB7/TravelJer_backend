import uuid
from typing import Dict, List, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field

from .chat import ChatManager
from .google_chat import GoogleGenAIChatModel

# --- Configuration ---
SECRET_KEY = "your-secret-key"  # In a real app, use a secure, environment-specific key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- FastAPI App Initialization ---
app = FastAPI()

# --- In-memory "Database" ---
db_users = {}
db_plans = {}
chat_managers: Dict[str, ChatManager] = {}

# --- Security ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# --- Pydantic Models ---

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
    place_details: PlaceDetails

class Persona(BaseModel):
    name: str
    backstory: str
    tone: str

class Conversation(BaseModel):
    role: str
    content: str
    timestamp: str

class Plan(BaseModel):
    plan_id: str
    user_id: str
    persona: Persona
    itinerary: List[ItineraryStop]
    conversation_history: List[Conversation]

class PlanCreate(BaseModel):
    style_id: str
    location: Location

class ChatMessage(BaseModel):
    message: str

# --- Helper Functions ---

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = db_users.get(token_data.email)
    if user is None:
        raise credentials_exception
    return user

# --- API Endpoints ---

@app.post("/api/auth/register", response_model=User)
async def register(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username in db_users:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(form_data.password)
    user = UserInDB(email=form_data.username, name=form_data.username, hashed_password=hashed_password)
    db_users[form_data.username] = user
    return User(email=user.email, name=user.name)

@app.post("/api/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db_users.get(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/plans", response_model=Plan)
async def create_plan(plan_data: PlanCreate, current_user: User = Depends(get_current_user)):
    plan_id = str(uuid.uuid4())
    
    # This is where you would call the Gemini API with the persona and tools
    # For now, we'll return a dummy plan
    
    dummy_persona = Persona(name="Auntie Lim", backstory="A friendly Peranakan auntie...", tone="Warm and motherly")
    dummy_itinerary = [
        ItineraryStop(
            stop=1,
            time="10:00",
            narrative="Come, lah, I know a place...",
            place_details=PlaceDetails(
                place_id="ChIJ...",
                display_name="Ah Hock's Char Kway Teow",
                formatted_address="123 Jalan Penang, George Town",
                location=Location(latitude=5.4174, longitude=100.3354),
                rating=4.5,
                user_rating_count=120,
                types=["restaurant", "food"]
            )
        )
    ]
    
    new_plan = Plan(
        plan_id=plan_id,
        user_id=current_user.email,
        persona=dummy_persona,
        itinerary=dummy_itinerary,
        conversation_history=[]
    )
    
    db_plans[plan_id] = new_plan
    
    # Initialize a chat manager for this plan
    model = GoogleGenAIChatModel(model_name='gemini-2.5-pro')
    chat_managers[plan_id] = ChatManager(chat_model=model)
    
    return new_plan

@app.get("/api/plans", response_model=List[Plan])
async def get_plans(current_user: User = Depends(get_current_user)):
    user_plans = [plan for plan in db_plans.values() if plan.user_id == current_user.email]
    return user_plans

@app.get("/api/plans/{plan_id}", response_model=Plan)
async def get_plan(plan_id: str, current_user: User = Depends(get_current_user)):
    plan = db_plans.get(plan_id)
    if not plan or plan.user_id != current_user.email:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan

@app.post("/api/plans/{plan_id}/chat", response_model=Plan)
async def chat_with_plan(plan_id: str, message: ChatMessage, current_user: User = Depends(get_current_user)):
    plan = db_plans.get(plan_id)
    if not plan or plan.user_id != current_user.email:
        raise HTTPException(status_code=404, detail="Plan not found")
        
    chat_manager = chat_managers.get(plan_id)
    if not chat_manager:
        raise HTTPException(status_code=500, detail="Chat manager not found for this plan")

    # Here you would call the LLM with the new message and context
    # For now, we'll just append the message and a dummy response
    
    plan.conversation_history.append(Conversation(role="user", content=message.message, timestamp="..."))
    
    # Dummy response from the AI
    dummy_response = "Of course! Not far from here is a café that overlooks the sea."
    plan.conversation_history.append(Conversation(role="assistant", content=dummy_response, timestamp="..."))
    
    # In a real implementation, the itinerary might be updated here
    
    return plan

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5004)