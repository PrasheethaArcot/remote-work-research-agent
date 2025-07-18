# src/graph/nodes.py
from langgraph.graph import StateGraph
from src.graph.state import ResearchState
from src.agents.research_planner import research_planner
from src.agents.synthesizer import synthesizer
from src.agents.document_processor import document_processor
from src.agents.report_generator import report_generator
from src.agents.information_gatherer import information_gatherer

# Register node functions
def plan_node(state: ResearchState) -> ResearchState:
    return research_planner(state)

def synthesize_node(state: ResearchState) -> ResearchState:
    return synthesizer(state)


def gather_info_node(state: ResearchState) -> ResearchState:
    return information_gatherer(state)



def document_processor_node(state: ResearchState) -> ResearchState:
    return document_processor(state)



def report_generator_node(state: ResearchState) -> ResearchState:
    return report_generator(state)



# Optional: add more wrappers later like gather_info, process_docs
