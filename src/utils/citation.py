# utils/citation_manager.py

from datetime import datetime
from urllib.parse import urlparse

# src/utils/citation.py
def cite_arxiv_paper(paper_data):
    """Generate citation for arXiv paper"""
    try:
        authors = paper_data.get('authors', ['Unknown Author'])
        if isinstance(authors, list):
            if len(authors) == 1:
                author_str = authors[0]
            elif len(authors) == 2:
                author_str = f"{authors[0]} and {authors[1]}"
            else:
                author_str = f"{authors[0]} et al."
        else:
            author_str = str(authors)
        
        title = paper_data.get('title', 'Unknown Title')
        published = paper_data.get('published', 'Unknown Date')
        pdf_url = paper_data.get('pdf_url', '')
        
        year = published[:4] if len(published) >= 4 else 'Unknown Year'
        
        citation = f"{author_str} ({year}). {title}. arXiv preprint. {pdf_url}"
        return citation
    except Exception as e:
        print(f"Error generating arXiv citation: {e}")
        return f"Citation error for: {paper_data.get('title', 'Unknown')}"

def cite_web_article(article_data):
    """Generate citation for web article"""
    try:
        title = article_data.get('title', 'Unknown Title')
        url = article_data.get('url', '')
        date = article_data.get('date', 'Unknown Date')
        source = article_data.get('source', 'Unknown Source')
        
        citation = f"{title}. {source}. {date}. {url}"
        return citation
    except Exception as e:
        print(f"Error generating web citation: {e}")
        return f"Citation error for: {article_data.get('title', 'Unknown')}"