# src/agents/information_gatherer.py
from typing import Dict

def information_gatherer(state: Dict) -> Dict:
    subtopics = state.get("subtopics", [])
    # Simulate document fetching for each subtopic
    documents = [f"Document content about {topic}" for topic in subtopics]
    state["documents"] = documents
    return state
