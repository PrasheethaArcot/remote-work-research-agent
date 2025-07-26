import streamlit as st
import re
from src.graph.runner import run_graph
from st_link_analysis import st_link_analysis, NodeStyle, EdgeStyle
from st_link_analysis.component.layouts import LAYOUTS

st.title("Research Agent")

query = st.text_input("Enter research topic:")

if st.button("Run Research"):
    if query:
        with st.spinner('Searching...'):
            steps_so_far = []
            steps_placeholder = st.empty()

            # Callback to update UI with completed steps
            def step_callback(step_name):
                steps_so_far.append(step_name.replace('_', ' ').title())
                steps_placeholder.markdown("**Steps completed:**\n" + "\n".join([f"- {s}" for s in steps_so_far]))

            # Run graph with initial state and callback
            initial_state = {"query": query}
            try:
                final_state = run_graph(initial_state, step_callback=step_callback)
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


    from st_link_analysis import st_link_analysis, NodeStyle, EdgeStyle

    # After final_state is returned from LangGraph
    query = final_state.get("query", "Research Query")
    subtopics = final_state.get("subtopics", [])
    agent_node_id = "agent"
    user_node_id = "user"

    nodes = [
        {"data": {"id": user_node_id, "label": "PERSON", "name": "User"}},
        {"data": {"id": agent_node_id, "label": "AGENT", "name": "Research Agent"}},
        {"data": {"id": "query", "label": "QUERY", "content": query}},
    ]

    # Add subtopic nodes
    for idx, topic in enumerate(subtopics):
        nodes.append({"data": {"id": f"sub_{idx}", "label": "SUBTOPIC", "content": topic}})

    edges = [
        {"data": {"id": "e1", "source": user_node_id, "target": "query", "label": "ASKS"}},
        {"data": {"id": "e2", "source": "query", "target": agent_node_id, "label": "HANDLED_BY"}},
    ]

    # Link agent to each subtopic
    for idx in range(len(subtopics)):
        edges.append({"data": {"id": f"e_sub_{idx}", "source": agent_node_id, "target": f"sub_{idx}", "label": "RESEARCHES"}})

    elements = {
        "nodes": nodes,
        "edges": edges,
    }

    # Define styles
    node_styles = [
    NodeStyle("PERSON", "#FF7F3E", "name", "person"),
    NodeStyle("AGENT", "#8B5CF6", "name", "hub"),  # Replaced `psychology` with valid one
    NodeStyle("QUERY", "#2A629A", "content", "help"),  # Replaced `help_outline` with `help`
    NodeStyle("SUBTOPIC", "#00A9A5", "content", "subject"),  # Replaced `notes` with valid one
    ]

    edge_styles = [
        EdgeStyle("ASKS", caption="label", directed=True),
        EdgeStyle("HANDLED_BY", caption="label", directed=True),
        EdgeStyle("RESEARCHES", caption="label", directed=True),
    ]

    # Render the graph
    st.markdown("### 📊 Research Graph")
    st_link_analysis(elements, layout="cose", node_styles=node_styles, edge_styles=edge_styles, height=600)




   

#PYTHONPATH=$(pwd) streamlit run src/ui/streamlit_app.py




   

#PYTHONPATH=$(pwd) streamlit run src/ui/streamlit_app.py
