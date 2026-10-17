import json
import chromadb
from sentence_transformers import SentenceTransformer
from chunk_pdf import load_pages, chunk_text

PDF_PATH = "data/rag_paper.pdf"
CONFIGS = [(400, 75), (800, 150), (1200, 200)]  # (chunk size, overlap)

model = SentenceTransformer("all-MiniLM-L6-v2")
pages = load_pages(PDF_PATH)
client = chromadb.EphemeralClient()  # temporary, in memory only

with open("eval_set.json", encoding="utf-8") as f:
    eval_set = json.load(f)


def run(size, overlap):
    chunks = []
    for page_num, text in pages:
        for c in chunk_text(text, size, overlap):
            chunks.append({"text": c, "page": page_num})

    texts = [c["text"] for c in chunks]
    col = client.create_collection(f"test_{size}_{overlap}")
    col.add(
        ids=[f"c{i}" for i in range(len(chunks))],
        documents=texts,
        embeddings=model.encode(texts).tolist(),
        metadatas=[{"page": c["page"]} for c in chunks],
    )

    rates = {}
    for k in (5, 10):
        hits = 0
        for item in eval_set:
            q = model.encode([item["question"]]).tolist()
            res = col.query(query_embeddings=q, n_results=k)
            hits += any(
                meta["page"] == item["page"] and item["answer_keyword"].lower() in doc.lower()
                for doc, meta in zip(res["documents"][0], res["metadatas"][0])
            )
        rates[k] = hits
    return len(chunks), rates


print("size | overlap | chunks | hit@5 | hit@10")
for size, overlap in CONFIGS:
    n, rates = run(size, overlap)
    print(f"{size} | {overlap} | {n} | {rates[5]}/{len(eval_set)} | {rates[10]}/{len(eval_set)}")