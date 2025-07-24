import arxiv

def test_arxiv_search():
    query = "quantum batteries"  # Replace with your test query
    search = arxiv.Search(
        query=query,
        max_results=3,
        sort_by=arxiv.SortCriterion.Relevance
    )

    papers = list(search.results())
    print(f"Found {len(papers)} papers:")
    for p in papers:
        print("-", p.title)

if __name__ == "__main__":
    test_arxiv_search()
