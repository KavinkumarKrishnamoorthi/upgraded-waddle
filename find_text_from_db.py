from langchain_community.vectorstores import FAISS

# Make sure your embedding model and vector DB are loaded
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db_path = "faiss_index"

# Load FAISS vectorstore
vectorstore = FAISS.load_local(db_path, embedding_model, allow_dangerous_deserialization=True)

# 🔍 Search query
query = "Maecenas"

# 🔎 Run similarity search with scores
results_with_scores = vectorstore.similarity_search_with_score(query, k=1)

# 🎯 Only show results with high enough similarity (you can tune this)
SIMILARITY_THRESHOLD = 0.9

# 🧪 Filter based on threshold
filtered_results = [(doc, score) for doc, score in results_with_scores if score >= SIMILARITY_THRESHOLD]

# 📦 Display results or nothing
if not filtered_results:
    print("No relevant matches found.")
else:
    for i, (res, score) in enumerate(filtered_results, start=1):
        print(f"\n=== Match {i} ===")
        print(f"Score: {score:.2f}")
        print("Matched Text:\n", res.page_content)
        print("Reference:\n", res.metadata)
