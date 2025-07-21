from src.utils.search_api import search_tavily, search_arxiv

def gather_information(state: dict) -> dict:
    subtopics = state.get("subtopics", [])
    all_results = []

    for subtopic in subtopics:
        print(f"Searching for: {subtopic}")

        web_results = search_tavily(subtopic, num_results=3)
        print(f"  Tavily returned {len(web_results)} results")

        arxiv_results = search_arxiv(subtopic, max_results=2)
        print(f"  arXiv returned {len(arxiv_results)} results")

        for r in web_results:
            r['source_type'] = 'web'
        for r in arxiv_results:
            r['source_type'] = 'arxiv'

        combined = web_results + arxiv_results
        all_results.extend(combined)

    print(f"Total gathered documents: {len(all_results)}")
    state["documents"] = all_results
    return state
