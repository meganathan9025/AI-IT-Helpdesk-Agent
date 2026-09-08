from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.tools import tool
from langchain.agents import create_agent


# -----------------------------
# 1. AI MODEL
# -----------------------------

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)


# -----------------------------
# 2. EMBEDDINGS
# -----------------------------

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# -----------------------------
# 3. CONNECT TO CHROMA
# -----------------------------

vectorstore = Chroma(
    collection_name="it_helpdesk",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)


# -----------------------------
# 4. RAG TOOL
# -----------------------------

@tool
def search_it_knowledge(query: str) -> str:
    """Search the IT support knowledge base for troubleshooting information."""

    results = vectorstore.similarity_search(query, k=3)

    if not results:
        return "No relevant information found."

    return "\n\n".join(
        result.page_content
        for result in results
    )


# -----------------------------
# 5. CREATE AGENT
# -----------------------------

agent = create_agent(
    model=llm,
    tools=[search_it_knowledge],
    system_prompt="""
You are an AI IT Helpdesk Agent.

Your job is to help users solve IT problems.

IMPORTANT:
- Always use the search_it_knowledge tool when the user
  asks about an IT troubleshooting problem.
- Use the information returned by the tool.
- Give clear numbered troubleshooting steps.
- Do not invent technical information.
- If the knowledge base does not contain enough information,
  clearly say so.
"""
)


# -----------------------------
# 6. USER QUESTION
# -----------------------------

question = (
    "My computer is connected to Wi-Fi but "
    "the internet is not working. What should I do?"
)


# -----------------------------
# 7. RUN AGENT
# -----------------------------

response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": question
        }
    ]
})


# -----------------------------
# 8. PRINT ANSWER
# -----------------------------

print("\n==============================")
print("       AI IT HELPDESK")
print("==============================\n")

print(response["messages"][-1].content)