#!/usr/bin/env python3
"""
Semantic query over the second brain. Returns the most relevant codex chunks.

    python .second-brain/rag/query.py "how does a segment tree lazy propagation work"
    python .second-brain/rag/query.py "explain useEffect cleanup" -k 8
"""
import sys, argparse, pathlib

HERE = pathlib.Path(__file__).resolve().parent
DB_DIR = HERE / "chroma_db"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="+")
    ap.add_argument("-k", type=int, default=5)
    args = ap.parse_args()
    q = " ".join(args.query)

    import chromadb
    from chromadb.utils import embedding_functions
    client = chromadb.PersistentClient(path=str(DB_DIR))
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2")
    col = client.get_collection("second_brain", embedding_function=ef)

    res = col.query(query_texts=[q], n_results=args.k)
    for i in range(len(res["ids"][0])):
        m = res["metadatas"][0][i]
        print(f"\n#{i+1}  {m['title']}  [{m['codex']}]")
        print(f"     {m['path']}")
        print("     " + res["documents"][0][i][:280].replace("\n", " "))


if __name__ == "__main__":
    main()
