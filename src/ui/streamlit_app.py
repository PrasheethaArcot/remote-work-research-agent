import streamlit as st
import re
import json
from src.graph.runner import run_graph
from st_link_analysis import st_link_analysis, NodeStyle, EdgeStyle
from st_link_analysis.component.layouts import LAYOUTS

st.set_page_config(page_title="Research Agent")
st.title("Research Agent")

# Two-tab layout
tab1, tab2 = st.tabs(["Research", "Knowledge Graph"])

with tab1:
    query = st.text_input("Enter research topic:")
    
    if st.button("Run Research"):
        if query:
            with st.spinner('Searching...'):
                steps_so_far = []
                steps_placeholder = st.empty()

                def step_callback(step_name):
                    steps_so_far.append(step_name.replace('_', ' ').title())
                    steps_placeholder.markdown("**Steps completed:**\n" + "\n".join([f"- {s}" for s in steps_so_far]))

                initial_state = {"query": query}
                try:
                    final_state = run_graph(initial_state, step_callback=step_callback)
                    # Store final_state in session state for graph tab
                    st.session_state["final_state"] = final_state
                except Exception as e:
                    st.error(f"Error running graph: {e}")
                    st.stop()

                steps_placeholder.markdown("**All steps completed:**\n" + "\n".join([f"- {s}" for s in steps_so_far]))
                st.success("Research completed!")

                # Extract outputs
                report = final_state.get("final_report") or final_state.get("report", "No report generated.")
                thinking = final_state.get("thinking", None)

                # Clean report
                thinking_block = None
                if report:
                    match = re.search(r'<think>(.*?)</think>', report, flags=re.DOTALL)
                    if match:
                        thinking_block = match.group(1).strip()
                        report = re.sub(r'<think>.*?</think>', '', report, flags=re.DOTALL)
                    report = re.sub(r'```.*?```', '', report, flags=re.DOTALL)
                    report = re.sub(r'\n##', r'\n\n##', report).strip()

                # Store research results in session state
                st.session_state["research_report"] = report
                st.session_state["thinking_block"] = thinking_block
                st.session_state["research_completed"] = True

                # Show model thinking first (right after steps completed)
                if thinking_block:
                    with st.expander("Model Thinking"):
                        st.markdown(thinking_block)

                # Show the research summary
                st.subheader("Research Summary")
                st.markdown(report)

        else:
            st.warning("Please enter a research topic.")

    # Show current research results if available
    if st.session_state.get("research_completed", False):
        st.markdown("---")
        st.subheader("Research Results")
        
        # Show model thinking if available
        thinking_block = st.session_state.get("thinking_block")
        if thinking_block:
            with st.expander("Model Thinking"):
                st.markdown(thinking_block)

        # Show the research summary
        report = st.session_state.get("research_report", "No report available.")
        st.markdown(report)

with tab2:
    import json
    import streamlit as st
    from st_link_analysis import st_link_analysis, NodeStyle, EdgeStyle
    from st_link_analysis.component.layouts import LAYOUTS

    LAYOUT_NAMES = list(LAYOUTS.keys())


    class DummyGraph:
        def __init__(self):
            self.load_data()
        
        def load_data(self):
            """Load data from data.json file"""
            try:
                with open("data.json", "r") as f:
                    elements = json.load(f)
                self.all_nodes = elements["nodes"]
                self.all_edges = elements["edges"]
                self.nodes = set([n["data"]["id"] for n in elements["nodes"]])
                self.edges = set([e["data"]["id"] for e in elements["edges"]])
                print(f"DEBUG: Loaded {len(self.all_nodes)} nodes and {len(self.all_edges)} edges from data.json")
            except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
                print(f"DEBUG: Error loading data.json: {e}")
                # Fallback to empty graph if data.json doesn't exist or is invalid
                st.warning("No valid data.json found. Run research first to generate graph data.")
                self.all_nodes = []
                self.all_edges = []
                self.nodes = set()
                self.edges = set()

        def get_elements(self):
            # Reload data before returning elements to ensure we have the latest
            self.load_data()
            return {
                "nodes": [n for n in self.all_nodes if n["data"]["id"] in self.nodes],
                "edges": [e for e in self.all_edges if e["data"]["id"] in self.edges],
            }

        def remove(self, node_ids):
            self.nodes -= set(node_ids)
            self._update_edges()

        def expand(self, node_ids):
            new_nodes = set()
            node_ids = set(node_ids)
            for e in self.all_edges:
                if e["data"]["source"] in node_ids:  # outbound
                    new_nodes.add(e["data"]["target"])
                elif e["data"]["target"] in node_ids:  # inbound
                    new_nodes.add(e["data"]["source"])
            self.nodes |= new_nodes
            self._update_edges()

        def _update_edges(self):
            self.edges = {
                e["data"]["id"]
                for e in self.all_edges
                if e["data"]["source"] in self.nodes and e["data"]["target"] in self.nodes
            }


    COMPONENT_KEY = "NODE_ACTIONS"

    if not hasattr(st.session_state, "graph"):
        st.session_state.graph = DummyGraph()

    layout = st.selectbox("Try with different layouts", LAYOUT_NAMES, index=0)

    # Dynamic node styles based on actual data
    def create_dynamic_node_styles(nodes):
        if not nodes:
            return []
        
        node_labels = set()
        for node in nodes:
            if "label" in node["data"]:
                node_labels.add(node["data"]["label"])
        
        colors = ["#FF7F3E", "#2A629A", "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#FFC107"]
        node_styles = []
        
        for i, label in enumerate(node_labels):
            color = colors[i % len(colors)]
            display_field = "name" if nodes and "name" in nodes[0]["data"] else "id"
            node_styles.append(NodeStyle(label, color, display_field, "description"))
        
        return node_styles

    # Dynamic edge styles based on actual data
    def create_dynamic_edge_styles(edges):
        if not edges:
            return []
        
        edge_labels = set()
        for edge in edges:
            if "label" in edge["data"]:
                edge_labels.add(edge["data"]["label"])
        
        edge_styles = []
        for label in edge_labels:
            edge_styles.append(EdgeStyle(label, caption='label', directed=True))
        
        return edge_styles

    elements = st.session_state.graph.get_elements()
    node_styles = create_dynamic_node_styles(elements["nodes"])
    edge_styles = create_dynamic_edge_styles(elements["edges"])


    def onchange_callback():
        val = st.session_state[COMPONENT_KEY]

        if val["action"] == "remove":
            st.session_state.graph.remove(val["data"]["node_ids"])

        elif val["action"] == "expand":
            st.session_state.graph.expand(val["data"]["node_ids"])


    with st.container(border=True):
        vals = st_link_analysis(
            elements,
            layout=layout,
            node_styles=node_styles,
            edge_styles=edge_styles,
            key=COMPONENT_KEY,
            node_actions=['remove', 'expand'],
            on_change=onchange_callback,
        )
        
        if vals:
            st.markdown("#### Returned Value")
            st.json(vals, expanded=True)

