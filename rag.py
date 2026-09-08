import re
import shutil
from pathlib import Path

from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


# ==========================================
# 1. LOAD KNOWLEDGE BASE
# ==========================================

file_path = Path("knowledge_base/it_support.txt")

text = file_path.read_text(encoding="utf-8").strip()


# ==========================================
# 2. FIND SECTION HEADINGS
# ==========================================

pattern = re.compile(
    r"(?m)^\s*(\d+)\.\s+([A-Z][A-Z ]+)\s*$"
)

matches = list(pattern.finditer(text))


documents = []


# ==========================================
# 3. CREATE ONE DOCUMENT PER SECTION
# ==========================================

for i, match in enumerate(matches):

    section_number = int(match.group(1))
    category = match.group(2).strip()

    start = match.start()

    if i + 1 < len(matches):
        end = matches[i + 1].start()
    else:
        end = len(text)

    section_text = text[start:end].strip()

    # Remove accidental duplicate consecutive lines
    lines = section_text.splitlines()

    cleaned_lines = []

    previous_line = None

    for line in lines:

        current_line = line.strip()

        if current_line == "":
            if cleaned_lines and cleaned_lines[-1] != "":
                cleaned_lines.append("")
            continue

        if current_line == previous_line:
            continue

        cleaned_lines.append(current_line)

        previous_line = current_line

    section_text = "\n".join(cleaned_lines).strip()

    documents.append(
        Document(
            page_content=section_text,
            metadata={
                "section": section_number,
                "category": category
            }
        )
    )


# ==========================================
# 4. DISPLAY SECTIONS
# ==========================================

print("==========================================")
print("KNOWLEDGE BASE SECTIONS")
print("==========================================")

for document in documents:

    print(
        f"Section {document.metadata['section']}: "
        f"{document.metadata['category']}"
    )

print("\nTotal sections:", len(documents))


# ==========================================
# 5. REMOVE OLD CHROMA DATABASE
# ==========================================

print("\nRemoving old Chroma database...")

shutil.rmtree(
    "./chroma_db",
    ignore_errors=True
)


# ==========================================
# 6. CREATE EMBEDDINGS
# ==========================================

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# ==========================================
# 7. CREATE VECTOR DATABASE
# ==========================================

vectorstore = Chroma(
    collection_name="it_helpdesk",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)


# ==========================================
# 8. STORE DOCUMENTS
# ==========================================

vectorstore.add_documents(documents)

print("\nKnowledge base successfully stored!")


# ==========================================
# 9. TEST RAG
# ==========================================

queries = [
    "My printer is not working",
    "My Wi-Fi is not working",
    "My computer is very slow"
]


for query in queries:

    print("\n==========================================")
    print("TEST QUERY")
    print("==========================================")

    print(query)

    results = vectorstore.similarity_search(
        query,
        k=1
    )

    if not results:

        print("\nNo relevant information found.")

        continue

    result = results[0]

    print("\nRetrieved Category:")
    print(result.metadata["category"])

    print("\nRetrieved Section:")
    print(result.page_content)