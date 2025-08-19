from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

# -----------------------------
# Step 1: Load the saved FAISS DB
# -----------------------------
embedding_model = OpenAIEmbeddings()
vectorstore = FAISS.load_local("faiss_index", embeddings=embedding_model, allow_dangerous_deserialization=True)

# -----------------------------
# Step 2: Ask a query
# -----------------------------
query = "the"

# Perform similarity search (top 3 most relevant chunks)
results = vectorstore.similarity_search(query, k=3)

# -----------------------------
# Step 3: Print results
# -----------------------------
for i, result in enumerate(results, 1):
    print(f"\nResult {i}")
    print("-" * 40)
    print("Content:", result.page_content)
    print("Metadata:", result.metadata)
