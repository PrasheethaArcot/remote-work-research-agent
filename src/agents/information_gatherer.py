from src.utils.search_api import search_serpapi, search_arxiv

def gather_information(state: dict) -> dict:
    """
    Searches the web and arXiv for each subtopic and gathers relevant results.
    Updates the state dict with a 'documents' key containing all results.
    """
    subtopics = state.get("subtopics", [])
    all_results = []

    for subtopic in subtopics:
        print(f"Searching for: {subtopic}")

        web_results = search_serpapi(subtopic, num_results=3)
        arxiv_results = search_arxiv(subtopic, max_results=2)

        # Tag results to help distinguish source
        for r in web_results:
            r['source_type'] = 'web'
        for r in arxiv_results:
            r['source_type'] = 'arxiv'

        combined = web_results + arxiv_results
        all_results.extend(combined)

    # Update state with gathered documents
    state["documents"] = all_results
    return state
