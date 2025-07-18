from typing import List, Tuple
from src.graph.state import ResearchState
from src.graph.edges import edges

def run_graph(initial_state: ResearchState) -> ResearchState:
    state = initial_state
    for from_node, to_node in edges:
        try:
            print(f"Running node: {from_node.__name__}")
            state = from_node(state)
            print(f"State after {from_node.__name__}: {state}\n")

            print(f"Running node: {to_node.__name__}")
            state = to_node(state)
            print(f"State after {to_node.__name__}: {state}\n")
        except Exception as e:
            print(f"Error in node {from_node.__name__} or {to_node.__name__}: {e}")
            break

    return state
