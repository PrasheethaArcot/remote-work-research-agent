# src/agents/synthesizer.py
import os
from dotenv import load_dotenv
from typing import Dict
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.utils.citation import cite_web_article, cite_arxiv_paper

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

    print(f"Received {len(documents)} processed texts")
    print(f"Received {len(citations)} citations:")
    for i, citation in enumerate(citations):
        print(f"  {i+1}. {citation}")

    # Join document texts
    if documents:
        docs_text = "\n\n".join(doc.get("text", "") for doc in documents[:5])
        print(f"Using processed texts: {len(docs_text)} characters")
    else:
        original_docs = state.get("results", []) or state.get("raw_documents", [])
        docs_text = "\n\n".join(doc.get("summary", "") for doc in original_docs[:5])
        print(f"Fallback to summaries: {len(docs_text)} characters")

    # Prepare prompt input
    inputs = {
        "subtopics": subtopics,
        "documents": docs_text
    }

    print("DEBUG: web_results =", state.get("web_results"))
    print("DEBUG: academic_results =", state.get("academic_results"))

    response = chain.invoke(inputs)
    report = response.content.strip()

    # Format citations into markdown
    def format_citation(c):
        authors = ", ".join(c.get("authors", []))
        return f"{c.get('title', 'Untitled')} ({c.get('published', 'n.d.')}) - {authors}. [PDF]({c.get('pdf_url', '#')})"

    citation_lines = [format_citation(c) for c in citations]

    if citation_lines:
        citation_text = "\n\n📚 Citations:\n" + "\n".join(f"- {line}" for line in citation_lines)
        print(f"Adding {len(citation_lines)} citations to report")
    else:
        citation_text = "\n\n📚 Citations:\n- No citations available."
        print("No valid citations found")

    report_with_citations = report + citation_text

    return {
        **state,
        "report": report_with_citations,
        "citations": citations,             
        "citation_lines": citation_lines    
    }
