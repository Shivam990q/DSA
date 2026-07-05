# 🧠 Memory Layer (mem0)

`memories.jsonl` holds atomic, self-contained memories about every document and
topic in the codices. Each line is one memory with rich metadata.

## Use with mem0
```bash
pip install mem0ai
python mem0_ingest.py        # loads every memory into mem0
```
Then any agent can recall:
```python
from mem0 import Memory
m = Memory()
m.search("how do I derive the master theorem", user_id="codex-second-brain")
```

## Use without mem0
`memories.jsonl` is plain JSONL — load it into any vector DB, SQLite, or feed it
directly to an LLM as retrieved context. It is the portable memory format.
