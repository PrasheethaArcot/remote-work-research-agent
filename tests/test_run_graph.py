from src.graph.runner import run_graph
from src.graph.state import ResearchState
import logging

logging.basicConfig(level=logging.DEBUG)
def main():
    initial_state = ResearchState(query="What are the latest trends in remote work?",)
    
    final_state = run_graph(initial_state)  # Run your nodes sequentially here
    
    print("Graph run successful!")
    print(final_state)
    print("\n🎯 Final Report:\n", final_state.get("report", "[No report generated]"))
    print("\n📚 Citations:\n", "\n".join(final_state.get("citations", [])))


if __name__ == "__main__":
    main()
