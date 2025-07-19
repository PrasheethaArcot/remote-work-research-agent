from typing import List, Tuple
from src.utils.documents import extract_text_from_pdf_url
from src.utils.citation import cite_web_article, cite_arxiv_paper
import logging

def document_processor(results: List[dict]) -> Tuple[List[str], List[str]]:
    texts = []
    citations = []

    for r in results:
        source_type = r.get("source_type", "")
        if source_type == "arxiv":
            pdf_url = r.get("pdf_url", "")
            if pdf_url:
                try:
                    full_text = extract_text_from_pdf_url(pdf_url)
                except Exception as e:
                    logging.warning(f"Failed to extract PDF from {pdf_url}: {e}")
                    full_text = "[Failed to extract PDF text]"
            else:
                full_text = "[No PDF URL provided]"
            texts.append(full_text)

            citation = cite_arxiv_paper(r)
            citations.append(citation)
            logging.debug(f"Arxiv citation generated: {citation}")

        elif source_type == "web":
            snippet = r.get("snippet", "[No snippet available]")
            texts.append(snippet)

            citation = cite_web_article(r)
            citations.append(citation)
            logging.debug(f"Web citation generated: {citation}")

        else:
            logging.info(f"Ignored result with unsupported source_type: {source_type}")

    logging.debug(f"Returning texts: {texts}")
    logging.debug(f"Returning citations: {citations}")

    return texts, citations
