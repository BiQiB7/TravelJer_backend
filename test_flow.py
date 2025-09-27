import requests
import json
import time
import os
from datetime import datetime

BASE_URL = "http://127.0.0.1:5004"

# --- Setup for logging ---
LOG_DIR = "test_outputs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE_PATH = os.path.join(LOG_DIR, f"test_run_{TIMESTAMP}.txt")

log_file = open(LOG_FILE_PATH, "w")

def log_and_print(message):
    """Prints to console and writes to log file."""
    print(message)
    log_file.write(str(message) + "\n")


def print_response(name, response):
    """Helper function to pretty-print JSON responses."""
    header = f"--- {name} ---"
    log_and_print(header)
    try:
        content = json.dumps(response.json(), indent=2)
        log_and_print(content)
    except json.JSONDecodeError:
        log_and_print(response.text)
    footer = "\n" + "="*50 + "\n"
    log_and_print(footer)

def main():
    # --- 1. Register a new user ---
    user_email = f"testuser_{int(time.time())}@example.com"
    user_password = "password123"
    register_response = requests.post(
        f"{BASE_URL}/api/auth/register",
        data={"username": user_email, "password": user_password}
    )
    print_response("1. Register User", register_response)

    # --- 2. Log in to get a token ---
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data={"username": user_email, "password": user_password}
    )
    print_response("2. Login", login_response)
    auth_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}

    # --- 3. Generate a Persona ---
    persona_payload = {
        "interests": ["history", "food"],
        "location": "Melaka"
    }
    persona_response = requests.post(f"{BASE_URL}/api/personas", json=persona_payload)
    log_and_print(persona_response)
    print_response("3. Generate Persona", persona_response)
    persona = persona_response.json()

    # --- 4. Create a Plan ---
    plan_payload = {
        "persona": persona,
        "location": {"latitude": 2.19, "longitude": 102.24} # Coordinates for Melaka
    }
    plan_response = requests.post(f"{BASE_URL}/api/plans", headers=headers, json=plan_payload)
    print_response("4. Create Plan", plan_response)
    plan = plan_response.json()
    plan_id = plan["plan_id"]

    # --- 5. Start a Conversation ---
    chat_payload_1 = {"message": "Hi! This plan looks great. What's the story behind the first stop?"}
    chat_response_1 = requests.post(f"{BASE_URL}/api/plans/{plan_id}/chat", headers=headers, json=chat_payload_1)
    print_response("5. Conversation - Step 1", chat_response_1)

    # --- 6. Ask for a change (re-plan) ---
    chat_payload_2 = {"message": "Actually, I'm not a big fan of crowds. Find a less touristy alternative."}
    chat_response_2 = requests.post(f"{BASE_URL}/api/plans/{plan_id}/chat", headers=headers, json=chat_payload_2)
    print_response("6. Conversation - Re-plan Request", chat_response_2)

    chat_payload_3 = {"message": "Yes, confirm the itinerary."}
    chat_response_3= requests.post(f"{BASE_URL}/api/plans/{plan_id}/chat", headers=headers, json=chat_payload_3)
    print_response("7. Confirm the plan", chat_response_3)
    
    # --- 7. Confirm the new plan ---
    if chat_response_2.json().get("draft_itinerary"):
        confirm_response = requests.post(f"{BASE_URL}/api/plans/{plan_id}/confirm", headers=headers)
        print_response("8. Confirm Update Plan", confirm_response)
    else:
        log_and_print("--- No draft itinerary was created, skipping confirmation. ---")


if __name__ == "__main__":
    try:
        main()
    finally:
        if 'log_file' in locals() and not log_file.closed:
            log_file.close()