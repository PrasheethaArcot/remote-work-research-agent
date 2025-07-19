from src.graph.edges import edges
from src.graph.state import ResearchState
from typing import Callable, List, Tuple

def run_graph(initial_state: ResearchState) -> ResearchState:
    state = initial_state
    
    # Build adjacency list from edges
    edge_map = {}
    for from_node, to_node in edges:
        edge_map.setdefault(from_node, []).append(to_node)
    
    # Find start nodes (nodes without any incoming edges)
    from_nodes = set(edge_map.keys())
    to_nodes = {node for targets in edge_map.values() for node in targets}
    start_nodes = list(from_nodes - to_nodes)
    
    if not start_nodes:
        raise RuntimeError("No start node found in graph")
    
    current_nodes = start_nodes
    
    while current_nodes:
        next_nodes = []
        for node in current_nodes:
            try:
                print(f"Running node: {node.__name__}")
                state = node(state)
                print(f"State after {node.__name__}: {state}\n")
                next_nodes.extend(edge_map.get(node, []))
            except Exception as e:
                print(f"Error in node {node.__name__}: {e}")
                return state
        current_nodes = next_nodes

    return state
