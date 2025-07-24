# src/ui/streamlit_app.py
import streamlit as st
from src.graph.runner import run_graph 

st.title("Research Agent")

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
            final_state = run_graph(initial_state, step_callback=step_callback)
            steps_placeholder.markdown("**All steps completed:**\n" + "\n".join([f"- {s}" for s in steps_so_far]))
            report = final_state.get("final_report") or final_state.get("report", "No report generated.")
            citations = final_state.get("citations", [])

            st.markdown(report)
    else:
        st.warning("Please enter a research topic.")

#PYTHONPATH=$(pwd) streamlit run src/ui/streamlit_app.py
