import json
from ask import retrieve

K = 5

with open("eval_set.json", encoding="utf-8") as f:
    eval_set = json.load(f)

hits = 0
for item in eval_set:
    results = retrieve(item["question"], k=K)
    found = any(
        meta["page"] == item["page"] and item["answer_keyword"].lower() in doc.lower()
        for doc, meta in results
    )
    hits += found
    print("HIT " if found else "MISS", "|", item["question"])

print(f"\nHit rate @ {K}: {hits}/{len(eval_set)} = {hits / len(eval_set):.0%}")