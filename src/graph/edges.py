# src/graph/edges.py
from typing import List, Tuple, Callable
from src.graph.state import ResearchState
from src.graph.nodes import plan_node, gather_info_node, document_processor_node, synthesize_node, report_generator_node

# Define an Edge as a callable that takes state and returns state
Edge = Callable[[ResearchState], ResearchState]

# List of edges to define the graph flow
# In this simple example: plan_node -> synthesize_node


edges = [
    (plan_node, gather_info_node),
    (gather_info_node, document_processor_node),
    (document_processor_node, synthesize_node),
    (synthesize_node, report_generator_node),
]


# You can expand this list later with more edges, e.g.
# (synthesize_node, gather_info_node), etc.
