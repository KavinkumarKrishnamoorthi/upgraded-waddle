from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

# -----------------------------
# Step 1: Load the saved FAISS DB
# -----------------------------
embedding_model = OpenAIEmbeddings(openai_api_key="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")
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
