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

# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a research assistant who writes structured summaries based on documents and subtopics."),
#     ("human", """
# Using the following documents, write a structured research summary covering these subtopics:

# Subtopics:
# {subtopics}

# Documents:
# {documents}

# Be concise, but cover all major points. Format with headings.
# """)
# ])
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a research assistant who writes detailed, structured, and clear summaries based on documents and subtopics."),
#     ("human", """
# Using the following documents, write a structured research summary covering these subtopics:

# Subtopics:
# {subtopics}

# Documents:
# {documents}

# For each subtopic:
# - Write a detailed paragraph explaining key points.
# - Include background, methods, findings, and implications if applicable.
# - Use examples or statistics where relevant.
# - Cite sources if citation info is provided.
# - Avoid unnecessary repetition, but do not be overly brief.
# - Use markdown headings for each subtopic.

# """)
# ])
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a research assistant skilled at synthesizing complex information into clear, accurate, and well-structured research summaries."),
    ("human", """
You are given a list of subtopics and a set of documents containing relevant information.

Task:
Write a comprehensive, structured research summary that covers each of the following subtopics in detail:

Subtopics:
{subtopics}

Documents:
{documents}

Instructions for each subtopic:
- Use markdown heading level 2 (i.e., '## Subtopic Name') for the subtopic title.
- Provide at least one detailed paragraph explaining the key concepts, background, methods, findings, and implications.
- When relevant, include specific examples, data points, or statistics extracted from the documents.
- Clearly explain any technical terms or jargon for a broad audience.
- Cite the sources by referencing document titles or URLs when specific information is included.
- Maintain a formal and objective tone.
- Avoid unnecessary repetition, but ensure completeness and clarity.
- Organize the summary logically, making it easy to follow.
- At the end, output a single overall confidence score (as a percentage between 0 and 100) based on how well the report is supported by the provided documents. Format the score like this:
Confidence Score: XX%

Deliver the summary in markdown format, ready for inclusion in a report.

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
