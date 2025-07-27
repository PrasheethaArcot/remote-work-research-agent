import streamlit as st
import re
from src.graph.runner import run_graph
from st_link_analysis import st_link_analysis, NodeStyle, EdgeStyle

st.title("Research Agent")

# Initialize session state for dynamic graph
if 'graph_data' not in st.session_state:
    st.session_state.graph_data = {
        'nodes': [],
        'edges': [],
        'execution_steps': []
    }

def create_dynamic_graph(state, step_name=None, execution_steps=None):
    """Create dynamic graph based on current state and execution step"""
    nodes = []
    edges = []
    
    # Use passed execution_steps or get from session state
    if execution_steps is None:
        execution_steps = st.session_state.graph_data.get('execution_steps', [])
    
    # Add user node
    nodes.append({"data": {"id": "user", "label": "PERSON", "name": "User"}})
    
    # Add query node
    query = state.get("query", "")
    if query:
        nodes.append({"data": {"id": "query", "label": "QUERY", "content": query[:50] + "..." if len(query) > 50 else query}})
        edges.append({"data": {"id": "user_query", "label": "SUBMITS", "source": "user", "target": "query"}})
    
    # Add ALL execution steps as nodes
    step_names = ["Plan Node", "Gather Info Node", "Document Processor Node", "Synthesize Node", "Report Generator Node"]
    
    # Debug: Show execution steps
    print(f"Execution steps: {execution_steps}")
    print(f"Number of execution steps: {len(execution_steps)}")
    
    for i, step_id in enumerate(execution_steps):
        if i < len(step_names):
            step_name_display = step_names[i]
        else:
            step_name_display = f"Step {i}"
        
        print(f"Adding step {i}: {step_id} -> {step_name_display}")
        nodes.append({"data": {"id": step_id, "label": "STEP", "content": step_name_display, "name": step_name_display}})
        
        # Connect steps in sequence
        if i == 0:  # First step connects from query
            edges.append({"data": {"id": f"query_{step_id}", "label": "TRIGGERS", "source": "query", "target": step_id}})
        else:  # Other steps connect from previous step
            prev_step = execution_steps[i-1]
            edges.append({"data": {"id": f"{prev_step}_{step_id}", "label": "FOLLOWS", "source": prev_step, "target": step_id}})
    
    # Add subtopics
    subtopics = state.get("subtopics", [])
    for i, subtopic in enumerate(subtopics):
        if isinstance(subtopic, str):
            clean_subtopic = subtopic[:30] + "..." if len(subtopic) > 30 else subtopic
            subtopic_id = f"subtopic_{i}"
            nodes.append({"data": {"id": subtopic_id, "label": "TOPIC", "content": clean_subtopic}})
            # Connect to planning step only if it exists
            if execution_steps and len(execution_steps) > 0:
                edges.append({"data": {"id": f"plan_{subtopic_id}", "label": "GENERATES", "source": execution_steps[0], "target": subtopic_id}})
    
    # Add document sources
    documents = state.get("documents", [])
    for i, doc in enumerate(documents[:5]):  # Limit to 5 docs for clarity
        if isinstance(doc, dict):
            title = doc.get("title", f"Document {i+1}")
            source_type = doc.get("source_type", "unknown")
            doc_id = f"doc_{i}"
            nodes.append({"data": {"id": doc_id, "label": "SOURCE", "content": title[:30] + "..." if len(title) > 30 else title, "source_type": source_type}})
            # Connect to search step only if it exists
            if len(execution_steps) > 1:
                edges.append({"data": {"id": f"search_{doc_id}", "label": "FINDS", "source": execution_steps[1], "target": doc_id}})
    
    # Add final report node
    if state.get("report"):
        nodes.append({"data": {"id": "report", "label": "REPORT", "content": "Final Research Report"}})
        if execution_steps and len(execution_steps) > 0:
            edges.append({"data": {"id": f"final_{execution_steps[-1]}_report", "label": "GENERATES", "source": execution_steps[-1], "target": "report"}})
        edges.append({"data": {"id": "report_user", "label": "DISPLAYS_TO", "source": "report", "target": "user"}})
    
    return {"nodes": nodes, "edges": edges, "execution_steps": execution_steps}

# Create tabs
tab1, tab2 = st.tabs(["Research", "Dynamic Workflow Graph"])

with tab1:
    query = st.text_input("Enter research topic:")

    if st.button("Run Research"):
        if query:
            # Reset graph data for new query
            st.session_state.graph_data = {
                'nodes': [],
                'edges': [],
                'execution_steps': []
            }
            
            with st.spinner('Searching...'):
                steps_so_far = []
                steps_placeholder = st.empty()

                # Callback to update UI with completed steps
                def step_callback(step_name):
                    steps_so_far.append(step_name.replace('_', ' ').title())
                    steps_placeholder.markdown("**Steps completed:**\n" + "\n".join([f"- {s}" for s in steps_so_far]))
                    
                    # Ensure execution_steps is maintained
                    if 'execution_steps' not in st.session_state.graph_data:
                        st.session_state.graph_data['execution_steps'] = []
                    
                    # Add the current step to execution_steps if not already present
                    if step_name not in st.session_state.graph_data['execution_steps']:
                        st.session_state.graph_data['execution_steps'].append(step_name)
                    
                    # Update graph in real-time
                    st.session_state.current_state = st.session_state.get('current_state', {"query": query})
                    graph_data = create_dynamic_graph(
                        st.session_state.current_state, 
                        step_name, 
                        st.session_state.graph_data['execution_steps']
                    )
                    st.session_state.graph_data = graph_data

                # Run graph with initial state and callback
                initial_state = {"query": query}
                try:
                    final_state = run_graph(initial_state, step_callback=step_callback)
                    st.session_state.current_state = final_state
                    
                    # Final graph update with complete state
                    final_graph_data = create_dynamic_graph(final_state, execution_steps=st.session_state.graph_data.get('execution_steps', []))
                    st.session_state.graph_data = final_graph_data
                    
                except Exception as e:
                    st.error(f"Error running graph: {e}")
                    st.stop()

                # Final step display
                steps_placeholder.markdown("**All steps completed:**\n" + "\n".join([f"- {s}" for s in steps_so_far]))

                # Extract outputs
                report = final_state.get("final_report") or final_state.get("report", "No report generated.")
                thinking = final_state.get("thinking", None)

                # Extract <think> block if present
                thinking_block = None
                if report:
                    match = re.search(r'<think>(.*?)</think>', report, flags=re.DOTALL)
                    if match:
                        thinking_block = match.group(1).strip()
                        report = re.sub(r'<think>.*?</think>', '', report, flags=re.DOTALL)
                    # Remove code blocks (triple backticks)
                    report = re.sub(r'```.*?```', '', report, flags=re.DOTALL)
                    # Ensure spacing before headings
                    report = re.sub(r'\n##', r'\n\n##', report).strip()

                # Show model thinking if available
                if thinking_block:
                    with st.expander("Model Thinking"):
                        st.markdown(thinking_block)

                # Show the final report as Markdown (for headings, bold, lists, etc.)
                st.markdown(report)

        else:
            st.warning("Please enter a research topic.")  

with tab2:
    st.header("Dynamic Workflow Graph")
    st.write("This graph shows the real-time execution of your research query and the relationships between components.")
    
    # Show current graph data
    if st.session_state.graph_data['nodes']:
        # Style node & edge groups for the main graph
        node_styles = [
            NodeStyle("PERSON", "#FF7F3E", "name", "person"),
            NodeStyle("QUERY", "#FF6B6B", "content", "description"),
            NodeStyle("STEP", "#4ECDC4", "content", "description"),
            NodeStyle("TOPIC", "#45B7D1", "content", "description"),
            NodeStyle("SOURCE", "#96CEB4", "content", "description"),
            NodeStyle("REPORT", "#FFEAA7", "content", "description"),
        ]

        edge_styles = [
            EdgeStyle("SUBMITS", caption='label', directed=True),
            EdgeStyle("TRIGGERS", caption='label', directed=True),
            EdgeStyle("FOLLOWS", caption='label', directed=True),
            EdgeStyle("GENERATES", caption='label', directed=True),
            EdgeStyle("FINDS", caption='label', directed=True),
            EdgeStyle("DISPLAYS_TO", caption='label', directed=True),
        ]

        st.markdown("### Live Research Workflow")
        st.write("Watch the graph update in real-time as your research progresses!")
        
        # Render the dynamic graph
        st_link_analysis(st.session_state.graph_data, "cose", node_styles, edge_styles, height=600)
        
    else:
        st.info("Run a research query in the 'Research' tab to see the dynamic graph in action!")
        
        # Show static demo graph
        st.markdown("### Demo Graph")
        st.write("Here's what the graph will look like when you run a query:")
        
        # Static demo data
        demo_elements = {
            "nodes": [
                {"data": {"id": 1, "label": "PERSON", "name": "User"}},
                {"data": {"id": 2, "label": "QUERY", "content": "Sample Query"}},
                {"data": {"id": 3, "label": "STEP", "content": "Planning"}},
                {"data": {"id": 4, "label": "STEP", "content": "Searching"}},
                {"data": {"id": 5, "label": "STEP", "content": "Synthesizing"}},
                {"data": {"id": 6, "label": "REPORT", "content": "Final Report"}},
            ],
            "edges": [
                {"data": {"id": 7, "label": "SUBMITS", "source": 1, "target": 2}},
                {"data": {"id": 8, "label": "TRIGGERS", "source": 2, "target": 3}},
                {"data": {"id": 9, "label": "FOLLOWS", "source": 3, "target": 4}},
                {"data": {"id": 10, "label": "FOLLOWS", "source": 4, "target": 5}},
                {"data": {"id": 11, "label": "GENERATES", "source": 5, "target": 6}},
                {"data": {"id": 12, "label": "DISPLAYS_TO", "source": 6, "target": 1}},
            ],
        }

        demo_node_styles = [
            NodeStyle("PERSON", "#FF7F3E", "name", "person"),
            NodeStyle("QUERY", "#FF6B6B", "content", "description"),
            NodeStyle("STEP", "#4ECDC4", "content", "description"),
            NodeStyle("REPORT", "#FFEAA7", "content", "description"),
        ]

        demo_edge_styles = [
            EdgeStyle("SUBMITS", caption='label', directed=True),
            EdgeStyle("TRIGGERS", caption='label', directed=True),
            EdgeStyle("FOLLOWS", caption='label', directed=True),
            EdgeStyle("GENERATES", caption='label', directed=True),
            EdgeStyle("DISPLAYS_TO", caption='label', directed=True),
        ]

        st_link_analysis(demo_elements, "cose", demo_node_styles, demo_edge_styles, height=400)




   

#PYTHONPATH=$(pwd) streamlit run src/ui/streamlit_app.py
