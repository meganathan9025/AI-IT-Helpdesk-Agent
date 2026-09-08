import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI IT Helpdesk Agent",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🤖 AI IT Helpdesk Agent")

st.markdown(
    """
    ### Intelligent IT Support Assistant

    Describe your IT problem below and the AI agent will
    diagnose the issue, use the knowledge base, and invoke
    MCP tools when required.
    """
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🛠 Helpdesk")

    st.markdown(
        """
        **Available Features**

        🔍 AI Troubleshooting  
        📚 Knowledge Base  
        🔧 MCP Diagnostics  
        🎫 Support Tickets  
        🖥 System Information  
        """
    )

    st.divider()

    st.info(
        "Powered by Ollama + RAG + MCP + LangGraph"
    )


# ============================================================
# CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# DISPLAY PREVIOUS MESSAGES
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ============================================================
# USER INPUT
# ============================================================

question = st.chat_input(
    "Describe your IT problem..."
)


# ============================================================
# PROCESS USER QUESTION
# ============================================================

if question:

    # --------------------------------------------------------
    # Display user message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)


    # --------------------------------------------------------
    # Temporary response
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "AI Helpdesk Agent is thinking..."
        ):

            response = (
                "👋 I received your request:\n\n"
                f"**{question}**\n\n"
                "The AI agent backend will be connected "
                "in the next step."
            )

            st.markdown(response)


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )