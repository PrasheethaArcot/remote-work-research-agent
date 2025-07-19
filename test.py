from utils.search_api import search_serpapi, search_arxiv
from utils.documents import extract_text_from_pdf_url
from utils.citation import cite_web_article, cite_arxiv_paper


# Define the research topic
topic = "effects of remote work on employee productivity"

# -----------------------------
# SerpAPI Web Search Results
# -----------------------------
print("SerpAPI Results:\n")
serp_results = search_serpapi(topic)

for idx, result in enumerate(serp_results, 1):
    print(f"{idx}. {result.get('title')}")
    print(f"   {result.get('link')}\n")

# -----------------------------
# arXiv Academic Search Results
# -----------------------------
print("\narXiv Results + Extracted PDF Text:\n")
arxiv_results = search_arxiv(topic)

for idx, paper in enumerate(arxiv_results, 1):
    print(f"{idx}. Title: {paper['title']}")
    print(f"   PDF: {paper['pdf_url']}")

    text = extract_text_from_pdf_url(paper['pdf_url'])
    preview = text[:300].strip().replace("\n", " ")

    print(f"   🧠 Preview: {preview}...")
    print("-" * 100)

# -----------------------------
# arXiv Academic Search Results
# -----------------------------
citation = cite_web_article(serp_results[0])
print("Citation:", citation)

citation = cite_arxiv_paper(arxiv_results[0])
print("Citation:", citation)
