from typing import TypedDict, List, Optional

class ResearchState(TypedDict):
    query: str
    subtopics: Optional[List[str]]
    documents: Optional[List[dict]]
    report: Optional[str]
    processed_texts: List[str]
    citations: List[str]
    recall_memories: Optional[List[str]] = []