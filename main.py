# main.py

import streamlit as st
from financial_agent import run_agent
from guardrails import moderate_input
# from logger import log_event
from config import DISCLAIMER

st.set_page_config(page_title="📊 Financial AI Copilot", page_icon="💼")
st.title("📊 Financial AI Copilot (Groq-Powered)")

st.markdown(DISCLAIMER)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat input
user_input = st.chat_input("Ask about stocks, terms, or financial news...")

if user_input:
    # log_event("user_input", user_input)  # Log it

    # 🔐 Apply guardrails
    moderation_result = moderate_input(user_input)
    if moderation_result:
        st.chat_message("assistant").write(moderation_result)
        # log_event("moderation_block", user_input)
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Thinking..."):
            try:
                response = run_agent(user_input)
                st.session_state.messages.append({"role": "assistant", "content": response})
                # log_event("agent_response", response)
            except Exception as e:
                error_message = f"❌ Something went wrong: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_message})
                # log_event("error", str(e))
                # log_event("error", str(e))

# Display messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
