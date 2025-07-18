# src/agents/document_processor.py
from typing import Dict
import re

def document_processor(state: Dict) -> Dict:
    documents = state.get("documents", [])

    # Simple cleaning: remove extra whitespace and unwanted characters
    cleaned_docs = []
    for doc in documents:
        # Remove multiple newlines and excess spaces
        text = re.sub(r'\s+', ' ', doc).strip()
        cleaned_docs.append(text)

    state["documents"] = cleaned_docs
    return state
