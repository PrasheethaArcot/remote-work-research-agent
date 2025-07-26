from src.utils.search_api import search_tavily, search_arxiv
import re

def gather_information(state: dict) -> dict:
    query = state.get("query", "")
    
    # Clean up query if it contains think blocks
    if "<think>" in query and "</think>" in query:
        print(f"⚠️  Found think block in query: {query[:50]}...")
        # Extract content after the think block
        think_match = re.search(r'<think>.*?</think>', query, flags=re.DOTALL)
        if think_match:
            print(f"   Think block content: {think_match.group(0)[:100]}...")
            query = query.replace(think_match.group(0), "").strip()
    
    subtopics = state.get("subtopics", [])
    all_results = []

    # Always search the original user query first
    search_terms = [query] if query else []
    # Then add subtopics (avoid duplicates)
    for subtopic in subtopics:
        if subtopic and subtopic not in search_terms:
            # Clean up subtopic if it contains think blocks
            clean_subtopic = subtopic
            if "<think>" in subtopic and "</think>" in subtopic:
                print(f"⚠️  Found think block in subtopic: {subtopic[:50]}...")
                think_match = re.search(r'<think>.*?</think>', subtopic, flags=re.DOTALL)
                if think_match:
                    print(f"   Think block content: {think_match.group(0)[:100]}...")
                    clean_subtopic = subtopic.replace(think_match.group(0), "").strip()
            if clean_subtopic and clean_subtopic not in search_terms:
                search_terms.append(clean_subtopic)

    for term in search_terms:
        # Clean up term if it contains think blocks
        clean_term = term
        if "<think>" in term and "</think>" in term:
            print(f"⚠️  Found think block in search term: {term[:50]}...")
            think_match = re.search(r'<think>.*?</think>', term, flags=re.DOTALL)
            if think_match:
                print(f"   Think block content: {think_match.group(0)[:100]}...")
                clean_term = term.replace(think_match.group(0), "").strip()
        
        if not clean_term:  # Skip empty terms
            continue
        
        # Truncate if too long
        if len(clean_term) > 400:
            print(f"⚠️  Search term too long (length {len(clean_term)}). Truncating to 400 characters.")
            clean_term = clean_term[:400]
        
        print(f"Searching for: {clean_term}")

        web_results = search_tavily(clean_term, num_results=5)
        print(f"  Tavily returned {len(web_results)} results")

        arxiv_results = search_arxiv(clean_term, max_results=2)
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
