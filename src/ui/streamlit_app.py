# src/ui/streamlit_app.py
import streamlit as st
from src.graph.runner import run_graph  # your function to run the graph

st.title("Research Agent")

query = st.text_input("Enter research topic:")

if st.button("Run Research"):
    if query:
        initial_state = {"query": query}
        final_state = run_graph(initial_state)
        report = final_state.get("final_report") or final_state.get("report", "No report generated.")
        st.markdown(report)
    else:
        st.warning("Please enter a research topic.")
