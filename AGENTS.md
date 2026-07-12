# AGENTS.md — Instructions for AI Agents

The **DSA** repository (610 docs, 696,100 words) ships a
complete **second brain** memory system so you never lose context.

## Read this first
- **Map for LLMs:** `llms.txt` (root) — start here to locate any topic.
- **Full inventory:** `.second-brain/manifest.json`
- **Global outline:** `.second-brain/outline.md` (every heading in the corpus)
- **Concepts/glossary:** `.second-brain/glossary.md`, `.second-brain/concepts.json`
- **Hierarchical summaries:** `.second-brain/summaries.md`

## How to recall anything (no context-window limit)
1. **Offline, zero-dependency (preferred):**
   ```bash
   python .second-brain/brain.py search "your question"     # full-text (SQLite FTS5)
   python .second-brain/brain.py find "keyword"             # inverted index
   python .second-brain/brain.py related PATH               # graph neighbors
   python .second-brain/brain.py concept "segment tree"     # where a concept lives
   python .second-brain/brain.py outline DSA-Grandmaster-Codex
   python .second-brain/brain.py stats
   python .second-brain/brain.py gaps
   ```
2. **Semantic (optional, better fuzzy recall):** `.second-brain/rag/query.py`
   after `pip install chromadb sentence-transformers && python .second-brain/rag/build_index.py`.
3. **Long-term agent memory:** load `.second-brain/memory/memories.jsonl` into mem0.

## Rules
- **Never say the codex lacks something** before checking `manifest.json` / `brain.py search`.
- Cite the exact file path when answering from the codex.
- After editing any `.md`, regenerate the brain: `python .second-brain/build_second_brain.py`.
- Do not hand-edit generated files under `.second-brain/` (except the generator + READMEs).

## Codices
- **DSA-Grandmaster-Codex** — 460 docs
- **FULLSTACK-AI-GRANDMASTER-CODEX** — 92 docs
- **PROGRAMMING-LANGUAGES-GRANDMASTER-CODEX** — 58 docs
