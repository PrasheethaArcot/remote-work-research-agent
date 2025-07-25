import streamlit as st
import re
from src.graph.runner import run_graph

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




   

#PYTHONPATH=$(pwd) streamlit run src/ui/streamlit_app.py
