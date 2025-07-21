# utils/search_apis.py
import os
from dotenv import load_dotenv
import arxiv
from tavily import TavilyClient
load_dotenv()



load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# search_tavily
def search_tavily(query, num_results=5):
    results = client.search(query=query, max_results=num_results)
    output = []

    for r in results.get("results", []):
        output.append({
            "title": r.get("title", ""),
            "text": r.get("content", ""),      
            "pdf_url": r.get("url", ""),       
            "authors": [],                      
            "published": "",                    
            "source_type": "web"
        })

    return output
# search_arxiv
import arxiv

def search_arxiv(query, max_results=3):
    client = arxiv.Client()

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    search_results = client.results(search)

    papers = []
    for result in search_results:
        papers.append({
            "title": result.title,
            "text": result.summary,
            "pdf_url": result.pdf_url,
            "authors": [a.name for a in result.authors],
            "published": str(result.published.date()),
            "source_type": "arxiv"
        })
    return papers




