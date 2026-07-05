---
inclusion: always
---
# 🧠 SECOND BRAIN — Permanent Memory (auto-generated, do not hand-edit)

> This file is injected into every conversation. It is my persistent memory of
> the **DSA** knowledge base in this workspace. When the user refers to
> "the system", "the engine", "the codex", or "the OS", they mean this.

## What exists here
- **576 documents**, **668,417 words**, across **3 codices** and **47 sections**.
- Full machine index: `.second-brain/manifest.json`
- Knowledge graph: `.second-brain/graph/knowledge-graph.json` (+ `graph.html` viewer)
- Long-term memory: `.second-brain/memory/memories.jsonl` (mem0-ready)
- Semantic retrieval (RAG): `.second-brain/rag/` (`build_index.py`, `query.py`)
- Obsidian vault: repo root is the vault; hubs in `.second-brain/obsidian/MOCs/`

## The codices
| Codex | Docs | Sections (partial) |
|-------|-----:|--------------------|
| `DSA-Grandmaster-Codex` | 460 | 00-PHILOSOPHY-AND-DOCTRINE, 01-LEVELS-PROGRESSION, 02-PROGRAMMING-FOUNDATIONS, 03-PROBLEM-SOLVING-FOUNDATIONS, 04-DATA-S |
| `FULLSTACK-AI-GRANDMASTER-CODEX` | 90 | 00-ROADMAP-AND-PHILOSOPHY, 01-WEB-FOUNDATIONS, 02-JAVASCRIPT-MASTERY, 03-TYPESCRIPT, 04-JAVA-MASTERY, 05-REACT, 06-NEXTJ |
| `PROGRAMMING-LANGUAGES-GRANDMASTER-CODEX` | 26 | 00-PHILOSOPHY-AND-DOCTRINE, 01-LANGUAGE-FOUNDATIONS, 02-PARADIGMS, 03-TYPE-SYSTEMS, 04-MEMORY-AND-RUNTIME, MASTER-INDEX. |

## How I use this memory (zero-dependency CLI — always works)
```
python .second-brain/brain.py ask "<natural language question>"   # semantic (TF-IDF)
python .second-brain/brain.py search "<keywords>"                 # full-text (SQLite FTS5)
python .second-brain/brain.py find "<keyword>"                    # inverted index
python .second-brain/brain.py code "<symbol>"                     # code-symbol search
python .second-brain/brain.py related <path>                      # graph neighbours
python .second-brain/brain.py concept "<term>"                    # where a concept lives
python .second-brain/brain.py outline|summary|stats|gaps|bridges|doctor
```
1. **To bootstrap fast**, read `.second-brain/context-pack.md` (whole codex, one file).
2. **Before answering codex questions**, run `brain.py ask/search` to find the exact
   owning file(s), then read them. Cite the path.
3. **Never claim the codex lacks something** without checking first (`ask`/`search`/manifest).
4. **After the codex changes**, regenerate: `python .second-brain/build_second_brain.py`
   (a Kiro fileEdited hook does this automatically on `.md` save).
5. **If anything seems off**, run `brain.py doctor` — it self-validates every artifact.
6. Treat `manifest.json` + graph + `tfidf-model.json` as the source of truth.

## Regeneration contract
This second brain is generated. If content drifts, rerun the generator. Do not
manually edit generated files under `.second-brain/` (except the generator and
the human READMEs).
