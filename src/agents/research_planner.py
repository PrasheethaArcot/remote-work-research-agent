# src/agents/research_planner.py
import os
from dotenv import load_dotenv
from typing import Dict
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

client = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-70b-8192"  
)


prompt = ChatPromptTemplate.from_messages([
    ("system", 
    """You are a world-class research analyst and investigative journalist.

For any research query—across science, sports, politics, technology, or culture—you identify the most important, newsworthy, and insightful subtopics.

For broad or ambiguous queries, always include:
- Recent events or developments
- Recent conflicts between historical places or people
- Key figures, organizations, or locations  
- Historical context or background  
- Major controversies, achievements, or milestones  
- Data, statistics, or performance highlights (if relevant)  
- Underlying causes, implications, or future directions  

Adapt subtopics to the domain of the query. For example:
- Sports: match summary, top performers, records  
- Science: mission goals, participants, discoveries, impact  

Rules:
- Output only a valid Python list of short string subtopics
- Do NOT include explanations, markdown, or formatting
- Do NOT inject hardcoded country names, events, or assumptions
- Infer what is most relevant for the query
"""),
    
    ("human", 
    """Break down the following research topic into 5–7 concise and meaningful subtopics.

Topic: {query}

Rules:
- Output a valid Python list of short string subtopics
- Do NOT include explanations, markdown, or formatting
- Do NOT add unrelated or speculative subtopics
- Stay tightly focused on the core aspects of the original topic

Example: ["Definition and Scope", "Current Trends", "Key Challenges", "Applications", "Future Directions"]
""")
])




chain = prompt | client

def research_planner(state: Dict) -> Dict:
    query = state["query"]
    response = chain.invoke({"query": query})
    try:
        subtopics = eval(response.content)
    except:
        subtopics = [response.content]
    return {**state, "subtopics": subtopics}
