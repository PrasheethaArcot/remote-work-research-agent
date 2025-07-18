# test_search.py
from utils.search_api import search_serpapi, search_arxiv

print("🔍 Web Search Results (SerpAPI):")
for result in search_serpapi("effects of remote work on productivity"):
    print(f"- {result.get('title')}")
    print(f"  {result.get('link')}\n")

print("\n📚 Academic Results (arXiv):")
for paper in search_arxiv("remote work productivity"):
    print(f"- {paper['title']}")
    print(f"  PDF: {paper['pdf_url']}")
    print(f"  Summary: {paper['summary'][:200]}...\n")
