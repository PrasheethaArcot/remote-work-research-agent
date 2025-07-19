from src.agents.document_processor import document_processor

sample_results = [
    {
        "source_type": "arxiv",
        "pdf_url": "http://arxiv.org/pdf/1234.5678v1",
        "title": "Sample Arxiv Paper",
        "authors": ["Alice Smith", "Bob Johnson"],
        "published": "2023-01-01"
    },
    {
        "source_type": "web",
        "snippet": "This is a snippet from a web article.",
        "title": "Sample Web Article",
        "link": "http://example.com/article"
    },
    {
        "source_type": "unknown",
        "snippet": "Should be ignored."
    }
]

texts, citations = document_processor(sample_results)
print("Texts:", texts)
print("Citations:", citations)
