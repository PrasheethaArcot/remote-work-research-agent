from typing import TypedDict, List, Optional

class ResearchState(TypedDict):
    query: str
    subtopics: Optional[List[str]]
    documents: Optional[List[str]]
    report: Optional[str]