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

    # Join document texts
    if documents and isinstance(documents[0], dict):
        docs_text = "\n\n".join(doc.get("text", "") for doc in documents[:5])
    else:
        docs_text = "\n\n".join(str(doc) for doc in documents[:5])

    inputs = {
        "subtopics": subtopics,
        "documents": docs_text
    }

    response = chain.invoke(inputs)
    report = response.content.strip()

    # Format citations into markdown
    def format_citation(c):
        authors = ", ".join(c.get("authors", []))
        title = c.get("title", "Untitled")
        published = c.get("published", "n.d.")
        pdf_url = c.get("pdf_url", "")
        if pdf_url:
            return f"{title} ({published}) - {authors}. [PDF]({pdf_url})"
        else:
            return f"{title} ({published}) - {authors}"

    if citations:
        citation_text = "\n\n📚 Citations:\n" + "\n".join(f"- {format_citation(c)}" for c in citations)
    else:
        citation_text = "\n\n📚 Citations:\n- No citations available."

    report_with_citations = report + citation_text

    return {
        **state,
        "report": report_with_citations,
        "citations": citations,
    }
