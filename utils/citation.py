# utils/citation_manager.py

from datetime import datetime
from urllib.parse import urlparse

def cite_web_article(result: dict) -> str:
    """
    Generate a basic APA-style citation for a web search result.
    """
    title = result.get("title", "Untitled")
    url = result.get("link", "")
    source = urlparse(url).netloc.replace("www.", "")
    year = datetime.now().year

    return f"{source}. ({year}). {title}. Retrieved from {url}"


def cite_arxiv_paper(paper: dict) -> str:
    """
    Generate an APA-style citation for an arXiv paper.
    """
    authors = paper.get("authors", [])
    title = paper.get("title", "Untitled")
    date = paper.get("published", "n.d.")
    year = date[:4] if date else "n.d."
    author_str = ", ".join(authors)
    pdf_url = paper.get("pdf_url", "")

    return f"{author_str} ({year}). {title}. arXiv. Retrieved from {pdf_url}"
