from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("sample.pdf")

# Get full plain text
full_text = result.document.export_to_text()

# Define your search term
search_word = "vehicula"

def search_with_page_info(document, keyword):
    results = []
    doc_dict = document.export_to_dict()
    for item in doc_dict["texts"]:
        if keyword.lower() in item["text"].lower():
            pages = [p.get("page_no") for p in item.get("prov", []) if p.get("page_no") is not None]
            results.append({"text": item["text"].strip(), "pages": pages or ["?"]})
    return results

matches = search_with_page_info(result.document, "vehicula")
for m in matches:
    print(f"On page(s) {m['pages']}: {m['text']}")