"""
Streamlit chat app for the fitness multi-agent system
"""
import streamlit as st
from dotenv import load_dotenv
from core.agentic_system import run_agent

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Fitness Buddy",
    page_icon="💪",
    layout="centered"
)

st.title("💪 Fitness Buddy")
st.caption("AI-powered fitness & nutrition assistant with Mastermind coordination")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        if msg["role"] == "assistant" and "logs" in msg:
            with st.expander("🔍 Agent reasoning (tool calls)"):
                for log in msg["logs"]:
                    st.markdown(log)

# Chat input
if prompt := st.chat_input("Ask about nutrition, workouts, or fitness..."):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        logs_placeholder = st.empty()

        with st.spinner("Thinking..."):
            try:
                answer, logs = run_agent("Mastermind", prompt)

                with message_placeholder.container():
                    st.markdown(answer)

                if logs:
                    with logs_placeholder.container():
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
