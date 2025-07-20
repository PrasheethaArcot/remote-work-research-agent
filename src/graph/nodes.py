# src/graph/nodes.py

from src.graph.state import ResearchState
from src.agents.research_planner import research_planner
from src.agents.synthesizer import synthesizer
from src.agents.document_processor import document_processor
from src.agents.report_generator import report_generator
from src.agents.information_gatherer import gather_information

# Register node functions
def plan_node(state: ResearchState) -> ResearchState:
    print("Running plan_node")
    return research_planner(state)

def synthesize_node(state: ResearchState) -> ResearchState:
    print("Running synthesize_node")
    return synthesizer(state)


def gather_info_node(state: ResearchState) -> ResearchState:
    print("Running gather_info_node")
    return gather_information(state)


def document_processor_node(state: ResearchState) -> ResearchState:
    results = state.get("results", []) or state.get("documents", [])
    print(f"Processing {len(results)} results...")
    for i, doc in enumerate(results[:3]):  
        print(f"Doc {i}: keys = {list(doc.keys())}")
    texts, citations = document_processor(results)
    state["documents"] = texts
    state["citations"] = citations
    return state


def report_generator_node(state: ResearchState) -> ResearchState:
    print("Running report_generator_node")
    return report_generator(state)



# Optional: add more wrappers later like gather_info, process_docs
