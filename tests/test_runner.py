# test_runner.py
from dotenv import load_dotenv
from src.graph.runner import run_graph

load_dotenv()

initial_state = {"query": "The impact of climate change on marine biodiversity"}

final_state = run_graph(initial_state)

print("Final report:\n")
print(final_state.get("report", "No report generated."))
