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
    ("system", "You are a research assistant who breaks down research topics."),
    ("human", """
Break down the following research topic into 5–7 concise subtopics.
Topic: {query}

Return ONLY a Python list of short strings. Example: ["Subtopic 1", "Subtopic 2", "Subtopic 3"]
Do NOT include explanations or markdown formatting.
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
