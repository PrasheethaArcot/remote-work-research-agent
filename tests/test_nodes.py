# test_nodes.py
import os
from dotenv import load_dotenv
from src.agents.research_planner import research_planner
from src.agents.synthesizer import synthesizer

load_dotenv()

# Step 1: test planner
initial_state = {"query": "The impact of climate change on marine biodiversity"}

print("Testing research_planner...\n")
state_after_planning = research_planner(initial_state)
print("Subtopics generated:")
print(state_after_planning["subtopics"])
print("\n")

# Step 2: test synthesizer (simulate dummy docs)
print("Testing synthesizer...\n")
state_after_planning["documents"] = [
    "Climate change causes ocean acidification which harms coral reefs.",
    "Warming oceans are leading to habitat loss for fish and marine mammals.",
    "Melting polar ice disrupts marine ecosystems and food chains."
]

final_state = synthesizer(state_after_planning)
print("Generated report:")
print(final_state["report"])
