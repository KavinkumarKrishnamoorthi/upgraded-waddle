from docling.document_converter import DocumentConverter

# Initialize the converter
converter = DocumentConverter()

# Path to your local PDF file
pdf_path = "sample.pdf"

# Convert to structured DoclingDocument
result = converter.convert(pdf_path)

# Export to Markdown
markdown_output = result.document.export_to_markdown()
print("----- Markdown Output -----")
print(markdown_output)

# Export to JSON
json_output = result.document.export_to_dict()
print("----- JSON Output -----")
print(json_output)
