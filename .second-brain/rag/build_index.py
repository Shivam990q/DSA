#!/usr/bin/env python3
"""
Build a local vector index from rag/chunks.jsonl for semantic retrieval.
This is what removes the "context window" limit: instead of loading the whole
codex, an agent retrieves only the few most relevant chunks per query.

Default backend: ChromaDB (local, no server) with sentence-transformers.
    pip install chromadb sentence-transformers

Run:
    python .second-brain/rag/build_index.py
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
CHUNKS = HERE / "chunks.jsonl"
DB_DIR = HERE / "chroma_db"


def main():
    import chromadb
    from chromadb.utils import embedding_functions

    client = chromadb.PersistentClient(path=str(DB_DIR))
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2")
    col = client.get_or_create_collection("second_brain", embedding_function=ef)

    ids, docs, metas = [], [], []
    with CHUNKS.open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            ids.append(r["id"])
            docs.append(r["text"])
            metas.append({k: r[k] for k in ("path", "title", "codex", "section")})

    B = 256
    for i in range(0, len(ids), B):
        col.upsert(ids=ids[i:i+B], documents=docs[i:i+B], metadatas=metas[i:i+B])
        print(f"  indexed {min(i+B, len(ids))}/{len(ids)}")
    print(f"[done] {len(ids)} chunks indexed into {DB_DIR}")


if __name__ == "__main__":
    main()
