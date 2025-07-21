from docling.document_converter import DocumentConverter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from sentence_transformers import SentenceTransformer
import os

# 1. Convert PDF to Text
converter = DocumentConverter()
result = converter.convert("sample.pdf")

# 2. Extract a section based on heading
def get_description_under_heading(document, heading_to_find):
    collecting = False
    result = []
    for item in document.texts:
        text = item.text.strip()
        if text.lower() == heading_to_find.lower():
            collecting = True
            continue
        if collecting and getattr(item, "is_heading", False):
            break
        if collecting:
            result.append(text)
    return result

heading = "In eleifend velit vitae libero sollicitudin euismod."
desc = get_description_under_heading(result.document, heading)
desc_text = "\n".join(desc)

# 3. Convert it into a Document for vector DB
doc = Document(
    page_content=desc_text,
    metadata={"source": "sample.pdf", "heading": heading}
)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
# 4. Initialize Embeddings and Vector DB
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents([doc], embedding_model)

# 5. Save Vector Store to Disk
db_path = "faiss_index"
vectorstore.save_local(db_path)

# 6. To search and retrieve later
new_vectorstore = FAISS.load_local(db_path, embedding_model)

query = "sollicitudin euismod description"
results = new_vectorstore.similarity_search(query, k=1)

# 7. Print Results with Reference
for res in results:
    print("Matched Text:\n", res.page_content)
    print("Reference:\n", res.metadata)
