# Experiment log

Eval set: 15 questions on the RAG paper (arXiv 2005.11401). Metric: hit rate (right page and keyword in the top-k chunks).
Setup: chunk size 800 chars, overlap 150, embedding model all-MiniLM-L6-v2, ChromaDB.

| # | Change | k | Hit rate |
|---|--------|---|----------|
| 1 | Baseline | 5 | 67% (10/15) |
| 2 | Retrieve more chunks | 10 | 93% (14/15) |

Notes:
- Misses at k=5 were table-based numbers, a vocabulary mismatch ("formulations" vs "models"), and one vague question.
- Larger k means more text sent to the LLM (higher cost, possible noise).