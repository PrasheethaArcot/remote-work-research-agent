# utils/search_apis.py
import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
import arxiv

load_dotenv()

def search_serpapi(query, num_results=5):
    params = {
        "q": query,
        "engine": "google",
        "api_key": os.getenv("SERPAPI_API_KEY"),
        "num": num_results
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get("organic_results", [])

def search_arxiv(query, max_results=3):
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    papers = []
    for result in search.results():
        papers.append({
            "title": result.title,
            "summary": result.summary,
            "authors": [a.name for a in result.authors],
            "pdf_url": result.pdf_url,
            "published": str(result.published.date())
        })
    return papers


