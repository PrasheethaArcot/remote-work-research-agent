# src/agents/synthesizer.py
import os
from dotenv import load_dotenv
from typing import Dict
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

client = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-70b-8192"  # Required
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a research assistant who writes structured summaries based on documents and subtopics."),
    ("human", """
Using the following documents, write a structured research summary covering these subtopics:

Subtopics:
{subtopics}

Documents:
{documents}

Be concise, but cover all major points. Format with headings.
""")
])

chain = prompt | client

def synthesizer(state: Dict) -> Dict:
    subtopics = state.get("subtopics", [])
    documents = state.get("documents", [])
    citations = state.get("citations", [])

    # Ensure documents are all strings
    documents = [doc if isinstance(doc, str) else str(doc) for doc in documents]

    # Join documents with two newlines
    docs_text = "\n\n".join(documents[:5])  # limit to first 5 docs

    # Prepare input variables for the prompt
    inputs = {
        "subtopics": subtopics,
        "documents": docs_text
    }

    response = chain.invoke(inputs)
    report = response.content.strip()
    print("Citations after synthesizer:", state.get("citations"))
    if not citations:
        citations = ["No citations available."]

    return {**state, "report": report, "citations": citations}

