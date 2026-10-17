from pypdf import PdfReader

reader = PdfReader("data/rag_paper.pdf")

print("Total pages:", len(reader.pages))
print("--- Page 1 text ---")
print(reader.pages[0].extract_text()[:500])