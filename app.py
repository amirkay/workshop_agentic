"""
Streamlit chat app for the fitness multi-agent system
"""
import streamlit as st
import os
from dotenv import load_dotenv
from core.agentic_system import create_fitness_graph, run_fitness_agent

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Fitness Buddy",
    page_icon="💪",
    layout="centered"
)

st.title("💪 Fitness Buddy")
st.caption("AI-powered fitness & nutrition assistant")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

api_key = os.getenv("OPENAI_API_KEY")

if "graph" not in st.session_state and api_key:
    with st.spinner("Initializing agent..."):
        st.session_state.graph = create_fitness_graph(api_key)

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        if msg["role"] == "assistant" and "logs" in msg:
            with st.expander("🔍 Agent reasoning (tool calls)"):
                for log in msg["logs"]:
                    st.markdown(log)

# Chat input
if prompt := st.chat_input("Ask something about fitness or nutrition"):
    if not api_key:
        st.error("OPENAI_API_KEY not found in environment.")
    else:
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    answer, logs = run_fitness_agent(
                        st.session_state.graph, prompt
                    )

                    st.markdown(answer)

                    if logs:
                        with st.expander("🔍 Agent reasoning (tool calls)"):
                            for log in logs:
                                st.markdown(log)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "logs": logs,
                        }
                    )

                except Exception as e:
                    st.error(str(e))
