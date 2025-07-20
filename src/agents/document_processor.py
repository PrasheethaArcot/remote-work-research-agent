from typing import List, Tuple, Dict
from src.utils.documents import extract_text_from_pdf_url
from src.utils.citation import cite_web_article, cite_arxiv_paper
import logging

def document_processor(results: List[dict]) -> Tuple[List[str], List[str]]:
    print(f"Processing {len(results)} documents...")
    texts = []
    citations = []

    for doc in results:
        content = doc.get("text") or doc.get("summary") or ""
        if not content.strip():
            continue  
        texts.append({"text": content, "source": doc.get("pdf_url", "")})
        citations.append({
            "title": doc.get("title", ""),
            "authors": doc.get("authors", []),
            "pdf_url": doc.get("pdf_url", ""),
            "published": doc.get("published", "")
        })

    return texts, citations


