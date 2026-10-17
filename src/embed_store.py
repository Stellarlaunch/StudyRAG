import chromadb
from sentence_transformers import SentenceTransformer
from chunk_pdf import build_chunks

PDF_PATH = "data/rag_paper.pdf"

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection("rag_paper")

if collection.count() == 0:
    chunks = build_chunks(PDF_PATH)
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts).tolist()
    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        documents=texts,
        embeddings=embeddings,
        metadatas=[{"page": c["page"], "source": c["source"]} for c in chunks],
    )
    print("Stored", len(chunks), "chunks")
else:
    print("Database already has", collection.count(), "chunks")

question = "What are the two RAG formulations?"
q_embedding = model.encode([question]).tolist()
results = collection.query(query_embeddings=q_embedding, n_results=3)

print("\nQuestion:", question)
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print("\n--- Page", meta["page"], "---")
    print(doc)