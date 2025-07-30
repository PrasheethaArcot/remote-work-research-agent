import streamlit as st
import re
from src.graph.runner import run_graph
from st_link_analysis import st_link_analysis, NodeStyle

st.set_page_config(page_title="Research Agent")
st.title("Research Agent")

# Two-tab layout
tab1, tab2 = st.tabs(["Research", "Dynamic Workflow Graph"])

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

                # Show model thinking first (right after steps completed)
                if thinking_block:
                    with st.expander("Model Thinking"):
                        st.markdown(thinking_block)

                # Show the research summary
                st.subheader("Research Summary")
                st.markdown(report)

        else:
            st.warning("Please enter a research topic.")

with tab2:
    st.subheader("Research Graph: Entities & Links")
    
    final_state = st.session_state.get("final_state", {})
    
    if final_state:
        subtopics = final_state.get("subtopics", [])
        documents = final_state.get("documents", [])
        query_text = final_state.get("query", "Research Query")

        nodes = [{"data": {"id": "query", "label": "QUERY", "title": query_text}}]
        edges = []

        for i, sub in enumerate(subtopics):
            sid = f"sub{i}"
            nodes.append({"data": {"id": sid, "label": "SUBTOPIC", "title": sub}})
            edges.append({"data": {"id": f"e_q_s{i}", "source": "query", "target": sid, "label": "HAS_SUBTOPIC"}})

        for i, doc in enumerate(documents):
            did = f"doc{i}"
            title = doc.get("title", f"Doc {i+1}")
            doc_data = {"id": did, "label": "DOCUMENT", "title": title}
            for k, v in doc.items():
                if isinstance(v, (str, float, int)):
                    doc_data[k] = v
            nodes.append({"data": doc_data})
            if "subtopic_index" in doc:
                sub_id = f"sub{doc['subtopic_index']}"
                edges.append({"data": {"id": f"e_s_d{i}", "source": sub_id, "target": did, "label": "CITED_BY"}})
            else:
                edges.append({"data": {"id": f"e_q_d{i}", "source": "query", "target": did, "label": "MENTIONS"}})

        node_styles = [
            NodeStyle("QUERY", "#FFC107", "title", "person"),
            NodeStyle("SUBTOPIC", "#00BCD4", "title", "description"),
            NodeStyle("DOCUMENT", "#8BC34A", "title", "description"),
        ]

        elements = {"nodes": nodes, "edges": edges}
        st_link_analysis(elements, layout="cose", node_styles=node_styles, key="research_graph")
    else:
        st.info("Run a research query in the Research tab to see the graph here.")

