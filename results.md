# Experiment log

Eval set: 15 questions on the RAG paper (arXiv 2005.11401). Metric: hit rate (right page and keyword in the top-k chunks).
Setup: chunk size 800 chars, overlap 150, embedding model all-MiniLM-L6-v2, ChromaDB.

| # | Change | Chunk size / overlap | k | Hit rate |
|---|--------|----------------------|---|----------|
| 1 | Baseline | 800 / 150 | 5 | 67% (10/15) |
| 2 | Retrieve more chunks | 800 / 150 | 10 | 93% (14/15) |
| 3 | Smaller chunks | 400 / 75 | 5 | 93% (14/15) |
| 4 | Larger chunks | 1200 / 200 | 5 | 60% (9/15) |

Notes:
- Misses at the baseline were table-based numbers, a vocabulary mismatch ("formulations" vs "models"), and one vague question.
- 400-char chunks at k=5 match the hit rate of 800-char chunks at k=10 while sending the LLM about 4x less text.
- All three chunk sizes reach 14/15 at k=10.
- Caveat: 15-question eval set; hit rate does not measure final answer correctness.