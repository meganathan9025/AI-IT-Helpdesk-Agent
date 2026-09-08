from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

vectorstore = Chroma(
    collection_name="it_helpdesk",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

print("Documents in database:", vectorstore._collection.count())

query = "My computer is connected to Wi-Fi but the internet is not working"

results = vectorstore.similarity_search(query, k=3)

print("\nNUMBER OF RESULTS:", len(results))

for i, result in enumerate(results, 1):
    print(f"\n--- Result {i} ---")
    print(result.page_content)