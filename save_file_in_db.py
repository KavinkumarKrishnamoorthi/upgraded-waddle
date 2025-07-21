import os
from docling.document_converter import DocumentConverter
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings

# Configuration
pdf_files = ["invoice1.pdf", "invoice2.pdf", "sample.pdf", "newsletter.pdf", "PrinceCatalogue.pdf","magic.pdf"]
search_word = "kavin"

# Initialize
converter = DocumentConverter()
all_documents = []

# Function to extract matching text with page info
def search_with_page_info(document, keyword):
    results = []
    doc_dict = document.export_to_dict()
    for item in doc_dict["texts"]:
        if keyword.lower() in item["text"].lower():
            pages = [p.get("page_no") for p in item.get("prov", []) if p.get("page_no") is not None]
            results.append({
                "text": item["text"].strip(),
                "pages": pages or ["?"]
            })
    return results

# Loop through PDFs
for pdf_path in pdf_files:
    print(f"📄 Processing: {pdf_path}")
    result = converter.convert(pdf_path)
    matches = search_with_page_info(result.document, search_word)

    for match in matches:
        doc = Document(
            page_content=match["text"],
            metadata={
                "source": os.path.basename(pdf_path),
                "pages": match["pages"]
            }
        )
        all_documents.append(doc)

print(f"✅ Total documents to store: {len(all_documents)}")

# Only save if we have documents
if all_documents:
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(all_documents, embedding_model)
    vectorstore.save_local("faiss_index")
    print("✅ FAISS vector DB created and saved.")
else:
    print("❌ No matching content found in any files.")
