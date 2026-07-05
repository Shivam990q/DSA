# 🧠 THE SECOND BRAIN — COMPLETE PLAYBOOK

> The portable, copy-paste memory system that makes **every project's AI sync
> absolute**. Drop it into any repo, run one command, and any AI (Kiro, Claude,
> Cursor, Copilot, ChatGPT, a local model) gains permanent, complete, no-context-
> limit recall of that project — forever.

This document explains **everything**, from the problem it solves to the last
line of code, plus exactly how to reuse it across all your other projects.

---

## 0. TL;DR — Put this in ANY project in 60 seconds

```bash
# 1. Copy ONE folder into your other project (only build_second_brain.py is required)
#    <your-project>/.second-brain/build_second_brain.py

# 2. Run it (Python 3.9+, standard library only — no pip installs)
python .second-brain/build_second_brain.py

# 3. Done. Ask the brain anything, from any AI or terminal:
python .second-brain/brain.py ask "how does auth work in this project"
```

That single file generates ~30 artifacts: a knowledge graph, semantic search,
full-text search, long-term memories, an Obsidian vault, `llms.txt`, `AGENTS.md`,
Kiro steering, fine-tune datasets, and a self-validating health check.

**The only file you must copy is `build_second_brain.py`.** Everything else is
regenerated from your project's content. It rewrites `brain.py` itself on every run.

---

## 1. THE PROBLEM THIS SOLVES

Every AI coding assistant has the same three failures:

1. **Context window limit** — it can't hold your whole project in memory. A
   650,000-word codebase does not fit in any context window. The AI sees a
   sliver and hallucinates the rest.
2. **Amnesia between sessions** — close the chat, and it forgets everything.
   Tomorrow it re-learns your project from scratch, badly.
3. **No structured recall** — even with RAG, the AI retrieves random text
   snippets. It doesn't understand how your concepts *relate* (multi-hop).

The Second Brain fixes all three by turning your project into a **queryable
external memory** the AI consults on demand, plus **always-on steering** that
keeps the map permanently in context.

> Core idea: **Retrieval is not memory.** RAG finds documents; memory *remembers
> structure*. This system does both — retrieval (RAG/TF-IDF/FTS) **and** memory
> (graph + triples + summaries + steering).

---

## 2. THE MENTAL MODEL — THREE PILLARS

```
                        THE SECOND BRAIN
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   NAVIGATION            RETRIEVAL               MEMORY
  (where is it?)       (find the text)      (remember structure)
        │                     │                     │
  manifest.json         tfidf-model.json      memories.jsonl (mem0)
  knowledge-graph       brain.db (FTS5)       graph triples
  outline.md            rag/ (vectors)        summaries (RAPTOR)
  glossary/concepts     inverted-index        Kiro steering (always-on)
  communities           llms-full.txt         history.jsonl
```

- **NAVIGATION** answers *"where does this live?"* — instant routing to the exact file.
- **RETRIEVAL** answers *"show me the relevant text"* — full-text, keyword, and semantic.
- **MEMORY** answers *"what is this and how does it connect?"* — structure that
  survives across sessions and is injected automatically.

An AI uses all three: navigate to the right area → retrieve the exact passages →
reason over the remembered structure.

---

## 3. HOW IT WORKS (the pipeline)

```
   YOUR REPO (.md + code files)
            │
            ▼
   build_second_brain.py  ── walks every file (robust: bad files skipped, never crashes)
            │
            ├── parses markdown  → title, headings, links, summary, word count
            ├── parses code      → symbols (functions/classes) per language
            ├── resolves links   → builds the edge list of the knowledge graph
            │
            ▼
   EMITS ~30 ARTIFACTS  (below), then SELF-VALIDATES (brain.py doctor)
            │
            ▼
   AI + humans query via brain.py / RAG / mem0 / Obsidian / MCP / llms.txt
```

Every run is **idempotent** — it regenerates everything from the live repo, so
the brain can never drift from the source of truth. A Kiro `fileEdited` hook
re-runs it automatically whenever you save a `.md` file.

---

## 4. EVERY ARTIFACT, EXPLAINED

All live under `.second-brain/` unless noted. Generated files should not be
hand-edited (rerun the generator instead).

### Navigation layer
| File | What it is | Why the AI needs it |
|------|-----------|---------------------|
| `manifest.json` | Full inventory: every doc's id, path, title, codex, section, topics, links, summary | The master index. First stop to find which file owns a topic. |
| `graph/knowledge-graph.json` | Nodes (codex/section/doc) + edges (contains/links) | Structural map; powers `related`. |
| `graph/graph.html` | Self-contained interactive graph viewer (vis-network via CDN) | Open in a browser to *see* the whole project. |
| `graph/graph.mermaid` | High-level domain tree in Mermaid | Paste into any Markdown/GitHub view. |
| `graph/communities.json` | Clusters of densely-linked docs + themes (GraphRAG-style) | Topic neighborhoods. |
| `graph/triples.json` | Subject–Predicate–Object facts (teaches/links_to/in_codex…) | Multi-hop reasoning ("what connects X and Y"). |
| `outline.md` / `outline.json` | The entire heading tree of every document | The full *shape* of the project at a glance. |
| `glossary.md` / `concepts.json` | Every concept → the docs that define/teach it | "Where is <concept> covered?" |
| `bridges.json` | Concepts shared across top-level areas | Cross-domain transfer. |
| `code-index.json` | Every code file + extracted symbols per language | Find a function/class fast. |

### Retrieval layer
| File | What it is | Why the AI needs it |
|------|-----------|---------------------|
| `brain.db` | SQLite + FTS5 full-text index of all chunks | Instant keyword/phrase search, **zero external deps**. |
| `tfidf-model.json` | Truncated TF-IDF unit vectors per doc | **Dependency-free semantic search** (`ask`). |
| `inverted-index.json` | term → doc list | Offline keyword fallback (`find`). |
| `rag/chunks.jsonl` | Heading-aware chunks of the whole corpus | Feed any vector DB / LLM context. |
| `rag/build_index.py` | Builds a Chroma vector index (optional) | Best fuzzy recall (needs `chromadb`). |
| `rag/query.py` | Semantic query CLI over the vector index | Natural-language retrieval. |
| `llms-full.txt` | The entire corpus concatenated | Single-fetch ingestion for large-context models. |

### Memory layer
| File | What it is | Why the AI needs it |
|------|-----------|---------------------|
| `memory/memories.jsonl` | Atomic, self-contained memories + metadata | Load into mem0 or any long-term store. |
| `memory/mem0_ingest.py` | Loads memories into mem0 | Permanent agent memory (needs `mem0ai`). |
| `summaries.md` / `summaries.json` | Rolled-up doc→section→codex summaries (RAPTOR-style) | Read the project at any zoom level. |
| `context-pack.md` | The whole project compressed into one file | Bootstrap any AI in one paste. |
| `history.jsonl` | A stats snapshot per build | Track growth over time. |

### Integration & agent layer (some at repo root)
| File | What it is |
|------|-----------|
| `../llms.txt` | The llmstxt.org standard — AI-agent corpus map at the repo root. |
| `../AGENTS.md` | Universal agent onboarding (read by Cursor, many agents, humans). |
| `../CLAUDE.md` | Pointer to AGENTS.md for Claude-based tools. |
| `../.kiro/steering/second-brain.md` | **Always injected** into Kiro's context — the AI's permanent map. |
| `../.kiro/steering/codex-navigation.md` | Always-on section routing cheat-sheet. |
| `mcp/mcp.example.json` | Config to expose memory via an MCP server. |
| `obsidian/MOCs/` + `../.obsidian/` | Obsidian vault (repo = vault) + Maps-of-Content hubs. |
| `../.vscode/tasks.json` | Editor tasks: rebuild / search / ask / doctor. |

### Tooling, quality & self-healing
| File | What it is |
|------|-----------|
| `brain.py` | The zero-dependency query engine (rewritten each build). |
| `build_second_brain.py` | The one generator. The only file you copy to reuse. |
| `coverage-report.md` | Orphans, stubs, missing indexes, TODO markers. |
| `broken-links.md` | Every dead internal link. |
| `validation-report.json` | Health check result (also via `brain.py doctor`). |
| `_scan-errors.log` | Any file that was skipped (too big / unreadable) — build never crashes. |
| `.cache/hashes.json` | Content hashes + added/changed/removed delta per run. |
| `schemas/` | JSON Schemas for the artifacts. |
| `training/finetune-*.jsonl` | Instruction + chat pairs for fine-tuning / eval. |
| `flashcards.jsonl` / `flashcards-anki.csv` | Q&A for spaced repetition + AI self-eval. |

---

## 5. THE `brain.py` COMMANDS (zero dependencies)

Run from anywhere in the repo. Works with only the Python standard library.

```bash
python .second-brain/brain.py ask "natural language question"   # SEMANTIC (TF-IDF cosine)
python .second-brain/brain.py search "keywords"                 # full-text (SQLite FTS5, BM25 ranked)
python .second-brain/brain.py find "keyword"                    # inverted-index keyword
python .second-brain/brain.py code "symbolName"                 # code-symbol search
python .second-brain/brain.py related <path>                    # graph neighbours of a doc
python .second-brain/brain.py triples <path>                    # facts about a doc
python .second-brain/brain.py bridges                           # cross-area shared concepts
python .second-brain/brain.py concept "term"                    # where a concept is taught
python .second-brain/brain.py outline [area]                    # heading tree
python .second-brain/brain.py summary [area]                    # hierarchical summaries
python .second-brain/brain.py doc <path>                        # one doc's full metadata
python .second-brain/brain.py stats                             # corpus statistics
python .second-brain/brain.py gaps                              # coverage report
python .second-brain/brain.py doctor                            # health / integrity self-check
python .second-brain/brain.py watch                             # auto-rebuild on file changes
```

**When to use which retrieval mode:**
- `ask` — you don't know the exact words ("how do I stop a race condition"). Best default.
- `search` — you know a phrase that appears verbatim.
- `find` — a single distinctive keyword.
- `code` — you want a function/class definition.

---

## 6. THE "AI ALWAYS REMEMBERS" MECHANISM (per tool)

Different tools read different files. This system feeds **all** of them:

| Tool | How it remembers | File |
|------|------------------|------|
| **Kiro** | Steering files injected into every conversation, automatically | `.kiro/steering/second-brain.md`, `codex-navigation.md` |
| **Cursor / many agents** | Reads `AGENTS.md` on entry | `AGENTS.md` |
| **Claude tools** | Reads `CLAUDE.md` → points to AGENTS.md | `CLAUDE.md` |
| **Web LLMs / crawlers** | The llms.txt standard | `llms.txt` (root) |
| **Any agent (live memory)** | mem0 long-term store | `memory/memories.jsonl` |
| **MCP-aware agents** | Memory exposed as MCP tools | `mcp/mcp.example.json` |
| **You (visual)** | Obsidian graph + Maps-of-Content | `.obsidian/`, `obsidian/MOCs/` |
| **Any terminal / script** | The zero-dep CLI | `brain.py` |

The workflow you teach every AI: **"Before answering anything about this
project, run `python .second-brain/brain.py ask '<question>'`, open the top
files, then answer and cite the path."** That line is already baked into
`AGENTS.md` and the Kiro steering.

---

## 7. DROP IT INTO ANOTHER PROJECT — STEP BY STEP

### Step 1 — Copy the generator
Copy `build_second_brain.py` into `<other-project>/.second-brain/`. That's the
only required file. (You can copy this `PLAYBOOK.md` too, for reference.)

### Step 2 — Run it
```bash
cd <other-project>
python .second-brain/build_second_brain.py
```
It auto-detects the project name from the folder (or set `SECOND_BRAIN_PROJECT`).
It indexes markdown **and** code (`.py .js .ts .java .cpp .go .rs .sql` …).

### Step 3 — Verify
```bash
python .second-brain/brain.py doctor      # should print HEALTHY
python .second-brain/brain.py stats
python .second-brain/brain.py ask "what does this project do"
```

### Step 4 — Keep it in sync (pick one)
- **Kiro**: a `fileEdited` hook on `**/*.md` runs the generator on save (this repo
  already has one; create the same in the new project's `.kiro/hooks/`).
- **Manual**: rerun the generator after big changes.
- **Watch**: `python .second-brain/brain.py watch` (polls and rebuilds).
- **Git**: add a pre-commit hook that runs the generator.

### Step 5 (optional) — Turn on heavy recall
```bash
pip install chromadb sentence-transformers   # vector RAG
python .second-brain/rag/build_index.py
python .second-brain/rag/query.py "a fuzzy question"

pip install mem0ai                            # persistent agent memory
python .second-brain/memory/mem0_ingest.py
```

**Dependency tiers:**
- **Tier 0 (always works, zero installs):** everything except `rag/build_index.py`,
  `rag/query.py`, `memory/mem0_ingest.py`. This includes semantic `ask` (pure-Python TF-IDF).
- **Tier 1 (optional):** Chroma vector RAG for sharper fuzzy recall.
- **Tier 2 (optional):** mem0 for cross-session live agent memory.

---

## 8. PORTABILITY NOTES & ASSUMPTIONS

- **Language of your project doesn't matter.** Markdown is indexed richly
  (headings, links, concepts); code files are indexed for symbols. Add more
  extensions in `CODE_EXT` if needed.
- **"Codex" = top-level folder.** The generator treats each top-level directory
  as a domain. For a normal code project, that becomes `src/`, `docs/`, etc. —
  still works, just relabeled. If you want docs-only, point it at a docs subtree.
- **Ignored automatically:** `.git`, `node_modules`, `.venv`, `__pycache__`,
  `.second-brain`, `.obsidian`, `.kiro`, `.idea`, `.vscode`. Extend `IGNORE_DIRS`.
- **Never crashes on bad input.** Files over 8 MB or unreadable are skipped and
  logged to `_scan-errors.log`. UTF-8 console output is forced.
- **No network, no telemetry, no external services** for Tier 0. Everything is local.

---

## 9. THE SYNC CONTRACT (why it never gets "fucked up")

1. The brain is a **projection** of your repo, not a second copy to maintain.
2. It is **regenerated whole** every run — no partial/stale state.
3. `brain.py doctor` **self-validates** every artifact after each build; if
   anything is missing or corrupt, it tells you (and `validation-report.json`
   records it).
4. `.cache/hashes.json` shows exactly what changed since last build.
5. Generated files carry a "do not hand-edit" note; the source of truth is your
   actual project files.

Result: the AI's memory is always an exact, current mirror of reality. There is
no drift, no rot, no forgotten context.

---

## 10. TROUBLESHOOTING

| Symptom | Fix |
|---------|-----|
| `ask` says "no known terms" | Query used only stopwords; try `search` or different words. |
| `search` returns nothing | Rebuild (`build_second_brain.py`) so `brain.db` exists; or FTS5 unavailable → it auto-falls back to LIKE. |
| Unicode error in console | Already handled (UTF-8 forced); if on an old Python, upgrade to 3.7+. |
| Counts look wrong after adding files | Rerun the generator; check `.cache/hashes.json` delta. |
| A file was skipped | See `_scan-errors.log` (too big or unreadable). |
| `doctor` shows PROBLEMS | Rerun the generator; if persistent, delete `brain.db` and rebuild. |

---

## 11. WHAT TO COPY (checklist)

To bless a new project with an "absolute" AI memory:

- [ ] `.second-brain/build_second_brain.py`  ← **required, the only must-copy file**
- [ ] `.second-brain/PLAYBOOK.md`  ← this guide (optional but handy)
- [ ] Run `python .second-brain/build_second_brain.py`
- [ ] (Kiro) create a `fileEdited` hook → `python .second-brain/build_second_brain.py`
- [ ] `python .second-brain/brain.py doctor` → confirm HEALTHY
- [ ] Commit the generated `AGENTS.md`, `llms.txt`, and `.second-brain/` (or gitignore
      the large generated blobs and keep just the generator — your choice)

That's it. Every project you touch now has a god-tier, self-healing, portable AI
memory that no context window can defeat.

---

*Generated system authored to be copied. One file in, total recall out.*
