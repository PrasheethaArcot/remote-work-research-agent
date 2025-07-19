# test_runner.py

from src.graph import build_graph

graph = build_graph()

initial_state = {
    "topic": "Effects of remote work on employee productivity",
    "subtopics": [
        "benefits of remote work",
        "challenges in productivity",
        "hybrid models impact"
    ]
}

result = graph.invoke(initial_state)

print("------FINAL OUTPUT------")
print("Extracted Texts:")
for t in result["texts"]:
    print(t[:300], "\n---\n")  # print first 300 chars

print("\nCitations:")
for c in result["citations"]:
    print("-", c)
