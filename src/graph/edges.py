from src.graph.state import ResearchState
from langgraph.graph import StateGraph
from src.graph.nodes import (
    plan_node,
    gather_info_node,
    document_processor_node,
    synthesize_node,
    report_generator_node,
)

def build_graph():
    graph = StateGraph(state_schema=ResearchState)

    # Register all nodes
    graph.add_node("plan_node", plan_node)
    graph.add_node("gather_info_node", gather_info_node)
    graph.add_node("document_processor_node", document_processor_node)
    graph.add_node("synthesize_node", synthesize_node)
    graph.add_node("report_generator_node", report_generator_node)

    # Set entry and finish nodes
    graph.set_entry_point("plan_node")
    graph.set_finish_point("report_generator_node")

    # Define edges (flow of execution)
    graph.add_edge("plan_node", "gather_info_node")
    graph.add_edge("gather_info_node", "document_processor_node")
    graph.add_edge("document_processor_node", "synthesize_node")
    graph.add_edge("synthesize_node", "report_generator_node")

    return graph.compile()

# Also export a plain edges list if you want to run manually
edges = [
    (plan_node, gather_info_node),
    (gather_info_node, document_processor_node),
    (document_processor_node, synthesize_node),
    (synthesize_node, report_generator_node),
]
