from pypdf import PdfReader

CHUNK_SIZE = 800   
OVERLAP = 150        


def load_pages(path):
    reader = PdfReader(path)
    return [(i + 1, page.extract_text() or "") for i, page in enumerate(reader.pages)]


def chunk_text(text, size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks


def build_chunks(path):
    all_chunks = []
    for page_num, text in load_pages(path):
        for chunk in chunk_text(text):
            all_chunks.append({"text": chunk, "page": page_num, "source": path})
    return all_chunks


if __name__ == "__main__":
    chunks = build_chunks("data/rag_paper.pdf")
    print("Total chunks:", len(chunks))
    print("--- Chunk 5 (page", chunks[5]["page"], ") ---")
    print(chunks[5]["text"])