from src.utils.search_api import search_tavily, search_arxiv

def gather_information(state: dict) -> dict:
    query = state.get("query", "")
    subtopics = state.get("subtopics", [])
    all_results = []

    # Always search the original user query first
    search_terms = [query] if query else []
    # Then add subtopics (avoid duplicates)
    for subtopic in subtopics:
        if subtopic and subtopic not in search_terms:
            search_terms.append(subtopic)

    for term in search_terms:
        print(f"Searching for: {term}")

        web_results = search_tavily(term, num_results=5)
        print(f"  Tavily returned {len(web_results)} results")

        arxiv_results = search_arxiv(term, max_results=2)
        print(f"  arXiv returned {len(arxiv_results)} results")

        for r in web_results:
            r['source_type'] = 'web'
        for r in arxiv_results:
            r['source_type'] = 'arxiv'

        combined = web_results + arxiv_results
        all_results.extend(combined)

    print(f"Total gathered documents: {len(all_results)}")
    state["documents"] = all_results
    state["raw_search_results"] = all_results  # For UI transparency
    return state
