#!/usr/bin/env python3
"""
Ingest the second brain into mem0 (https://github.com/mem0ai/mem0) so any AI
agent has permanent, searchable long-term memory of the entire codex.

    pip install mem0ai

Local (open-source) usage stores memories in a local vector store.
Set OPENAI_API_KEY (or configure another LLM/embedder) per mem0 docs.

    python .second-brain/memory/mem0_ingest.py
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
MEMORIES = HERE / "memories.jsonl"
USER_ID = "codex-second-brain"


def main():
    from mem0 import Memory
    m = Memory()
    n = 0
    with MEMORIES.open(encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            m.add(rec["memory"], user_id=USER_ID, metadata=rec.get("metadata", {}))
            n += 1
            if n % 100 == 0:
                print(f"  added {n} memories")
    print(f"[done] {n} memories added to mem0 under user_id='{USER_ID}'")
    print("Query with:  m.search('your question', user_id='%s')" % USER_ID)


if __name__ == "__main__":
    main()
