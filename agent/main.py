# from src.agent_service.agent import BaseAgent
# from src.agent_service.tools import tools
from agent import BaseAgent
from tools import tools
import datetime
print(tools)
agent = BaseAgent(tools=tools)

# --- Example Persona ---
persona = {
    "name": "Auntie Lim",
    "backstory": "A friendly Peranakan 'auntie' who has run a small sundry shop in George Town for 30 years. She knows every hawker stall owner by name.",
    "tone": "Warm, motherly, full of 'insider' tips."
}

# --- Constructing the System Prompt from the Persona ---
system_prompt = f"""
You are {persona['name']}, a {persona['tone']} tour guide.
Your backstory: {persona['backstory']}
You are helping a user plan a trip.
"""

# --- Example Human Prompt ---
human_prompt = "Hi Auntie Lim, can you suggest a good place for Char Kway Teow in Penang?"

print(f"--- System Prompt ---\n{system_prompt}")
print(f"--- Human Prompt ---\n{human_prompt}\n")
print("--- Agent Output ---")

for step in agent.run(human_prompt, system_prompt):
    print(step)

