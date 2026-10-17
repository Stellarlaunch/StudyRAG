import os
import chromadb
from dotenv import load_dotenv
from google import genai
from sentence_transformers import SentenceTransformer

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
db = chromadb.PersistentClient(path="chroma_db")
collection = db.get_collection("rag_paper")


def retrieve(question, k=5):
    q_emb = embed_model.encode([question]).tolist()
    res = collection.query(query_embeddings=q_emb, n_results=k)
    return list(zip(res["documents"][0], res["metadatas"][0]))


def answer(question):
    hits = retrieve(question)
    context = "\n\n".join(
        f"[Page {meta['page']}]\n{doc}" for doc, meta in hits
    )
    prompt = (
        "Answer the question using ONLY the context below. "
        "Mention the page numbers you used. "
        "If the answer is not in the context, say you don't know.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}"
    )
    response = client.models.generate_content(
        model="gemini-3.8-flash", contents=prompt
    )
    pages = sorted({meta["page"] for _, meta in hits})
    return response.text, pages


if __name__ == "__main__":
    q = input("Ask a question: ")
    text, pages = answer(q)
    print("\nAnswer:\n", text)
    print("\nSources: pages", pages)