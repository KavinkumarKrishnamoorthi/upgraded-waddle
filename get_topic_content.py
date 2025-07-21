import sys
import os
sys.path.append(r"P:\projects\upgraded-waddle")

from docling.document_converter import DocumentConverter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document

# 1. Initialize converter
converter = DocumentConverter()

# 2. Set paths and inputs
pdf_path = "newsletter.pdf"  # Adjust if reading from folder
target_headings = ["Muscle Spindles"]

# 3. Convert PDF
result = converter.convert(pdf_path)

# 4. Extract section text by heading
def get_description_under_heading(document, heading):
    collecting = False
    lines = []
    for item in document.texts:
        text = item.text.strip()
        if text.lower() == heading.lower():
            collecting = True
            continue
        if collecting and getattr(item, "is_heading", False):
            break
        if collecting:
            lines.append(text)
    return "\n".join(lines)

# 5. Collect documents if text found
all_documents = []
for heading in target_headings:
    desc_text = get_description_under_heading(result.document, heading)
    if desc_text.strip():  # Make sure it's not empty
        doc = Document(
            page_content=desc_text,
            metadata={"source": pdf_path, "heading": heading}
        )
        all_documents.append(doc)
    print("--------------------------------------",type(all_documents)) # Should print: <class 'langchain.schema.document.Document'>
# 6. Only proceed if at least one document has content
if all_documents:
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(all_documents, embedding_model)
    vectorstore.save_local("faiss_index")
else:
    print("⚠️ No valid sections found. Vector DB not created.")
    exit()

# 7. Reload vector DB
vectorstore = FAISS.load_local("faiss_index", embedding_model, allow_dangerous_deserialization=True)

# 8. Search query and filter by score
query = "Etiam"
results = vectorstore.similarity_search_with_score(query, k=3)
THRESHOLD = 0.7  # Customize threshold for relevance

filtered = [(doc, score) for doc, score in results if score >= THRESHOLD]

# 9. Print filtered results
if not filtered:
    print("❌ No relevant match found.")
else:
    for doc, score in filtered:
        print("✅ Match Found")
        print("Source:", doc.metadata)
        print("Excerpt:", doc.page_content[:150], "...\n")
