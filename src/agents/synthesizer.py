import os
from dotenv import load_dotenv
from typing import Dict
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

client = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="deepseek-r1-distill-llama-70b" 
)


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a research assistant skilled at synthesizing complex information into clear, accurate, and well-structured research summaries."),
    ("human", """
You are given a list of subtopics and a set of documents containing relevant information, including results from real-time web search (Tavily) and academic sources (arXiv).

Your task is to write a comprehensive, structured research summary that addresses each subtopic in detail **using only the information provided**. Do **not** make up or infer information that is not explicitly found in the documents.

Subtopics:
{subtopics}

Documents:
{documents}

Instructions:
- For each subtopic, use markdown heading level 2 (i.e., '## Subtopic Name') as the section title.
- Write at least one detailed paragraph per subtopic covering: background, key concepts, methods, findings, and implications.
- When relevant, include specific examples, data points, or statistics from the documents.
- If a subtopic is only partially covered, clearly state the gap and lower the confidence score accordingly.
- Clearly explain any technical terms or jargon for a broad audience.
- Ignore documents that are irrelevant to the subtopics.
- Maintain a formal, objective tone. Avoid repetition, but ensure completeness.
- Organize subtopics logically.

At the end of the report, output a **Confidence Score** (as a percentage between 0 and 100), formatted like this:

Confidence Score: XX%

Deliver the output in markdown format, suitable for inclusion in a report.
""")
])

chain = prompt | client

def synthesizer(state: Dict) -> Dict:    
    subtopics = state.get("subtopics", [])
    documents = state.get("documents", [])  
    citations = state.get("citations", [])
    recall_memories = state.get("recall_memories", [])

    # Join document texts
    if documents and isinstance(documents[0], dict):
        docs_text = "\n\n".join(doc.get("text", "") for doc in documents[:5])
    else:
        docs_text = "\n\n".join(str(doc) for doc in documents[:5])

    recall_text = "\n".join(recall_memories)

    inputs = {
        "subtopics": subtopics,
        "documents": docs_text + "\n\n[Recall Memories]\n" + recall_text
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
            return f"{title} ({published}) - {authors}. [Link]({pdf_url})"
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
