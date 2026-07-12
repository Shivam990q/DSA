#!/usr/bin/env python3
"""
================================================================================
  THE SECOND BRAIN  ·  Master Generator
================================================================================
One script to build the entire persistent-memory system for the codices.

It walks the whole repository, understands every markdown file (title, headings,
links, domain, size), and emits a complete, machine + human + AI readable memory
system:

    manifest.json            full inventory of every knowledge atom
    graph/knowledge-graph.json  nodes + edges (the "graphify" layer)
    graph/graph.html            interactive, self-contained graph viewer
    graph/graph.mermaid         high-level domain map
    memory/memories.jsonl       mem0-style atomic memories
    rag/chunks.jsonl            chunked corpus for vector / RAG retrieval
    obsidian/MOCs/*.md          Obsidian Maps-of-Content (wikilink hubs)
    .obsidian/                  Obsidian vault config (repo root = vault)
    ../.kiro/steering/*.md      always-on memory for the Kiro AI

Run:
    python .second-brain/build_second_brain.py

Idempotent: safe to run repeatedly. Regenerates everything from the live repo,
so the second brain never drifts from the source of truth.
================================================================================
"""
from __future__ import annotations

import json
import os
import re
import sys
import hashlib
import datetime
from pathlib import Path

try:                                   # never let console encoding crash a build
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# --------------------------------------------------------------------------- #
#  Paths & configuration
# --------------------------------------------------------------------------- #
SCRIPT_DIR = Path(__file__).resolve().parent          # .../<project>/.second-brain
REPO_ROOT = SCRIPT_DIR.parent                          # .../<project>
BRAIN = SCRIPT_DIR
# Project name is auto-derived so this generator is 100% portable: drop the
# .second-brain folder into ANY repo, run it, and everything self-labels.
PROJECT_NAME = os.environ.get("SECOND_BRAIN_PROJECT", REPO_ROOT.name)
GRAPH_DIR = BRAIN / "graph"
MEM_DIR = BRAIN / "memory"
RAG_DIR = BRAIN / "rag"
OBS_MOC_DIR = BRAIN / "obsidian" / "MOCs"
KIRO_STEERING = REPO_ROOT / ".kiro" / "steering"
OBSIDIAN_CFG = REPO_ROOT / ".obsidian"

# directories we never scan (generated / vcs / tooling)
IGNORE_DIRS = {".git", ".second-brain", ".obsidian", ".kiro", "_javacheck",
               "node_modules", "__pycache__", ".idea", ".vscode"}
# generated meta-files that must never be indexed as knowledge atoms
IGNORE_FILES = {"AGENTS.md", "CLAUDE.md", "llms.txt", "llms-full.txt"}

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
MDLINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
CODEFENCE_RE = re.compile(r"^```")
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()


def rel(p: Path) -> str:
    return str(p.relative_to(REPO_ROOT)).replace("\\", "/")


def slug(text: str) -> str:
    s = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[\s_]+", "-", s)


def node_id(path_rel: str) -> str:
    return "doc:" + hashlib.sha1(path_rel.encode("utf-8")).hexdigest()[:12]


# --------------------------------------------------------------------------- #
#  Domain detection — the top-level "kingdoms" of the codex
# --------------------------------------------------------------------------- #
def domain_of(path_rel: str) -> tuple[str, str]:
    """Return (codex, section) for a given relative path."""
    parts = path_rel.split("/")
    codex = parts[0] if parts else "root"
    section = parts[1] if len(parts) > 1 else "(root)"
    return codex, section


# --------------------------------------------------------------------------- #
#  Parse a single markdown file into a knowledge atom
# --------------------------------------------------------------------------- #
def parse_markdown(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    title = None
    headings = []          # (level, text)
    in_fence = False
    for ln in lines:
        if CODEFENCE_RE.match(ln.strip()):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(ln)
        if m:
            level = len(m.group(1))
            htext = m.group(2).strip()
            headings.append((level, htext))
            if title is None and level == 1:
                title = htext

    path_rel = rel(path)
    if title is None:
        title = path.stem.replace("-", " ")

    # outgoing links (markdown + wikilink)
    md_links = MDLINK_RE.findall(text)
    wiki_links = WIKILINK_RE.findall(text)

    out_links = []
    for _label, target in md_links:
        t = target.strip()
        if t.startswith("http") or t.startswith("#") or t.startswith("mailto:"):
            continue
        out_links.append(t.split("#")[0])
    for w in wiki_links:
        out_links.append(w.split("|")[0].split("#")[0])

    words = len(re.findall(r"\S+", text))
    codex, section = domain_of(path_rel)

    # first meaningful non-heading, non-quote paragraph = summary seed
    summary = ""
    for ln in lines:
        s = ln.strip()
        if not s or s.startswith("#") or s.startswith(">") or s.startswith("---") \
                or s.startswith("```") or s.startswith("|") or s.startswith("*") \
                or s.startswith("-"):
            continue
        summary = s
        break

    return {
        "id": node_id(path_rel),
        "path": path_rel,
        "title": title,
        "codex": codex,
        "section": section,
        "words": words,
        "headings": [{"level": l, "text": t} for l, t in headings],
        "h2": [t for l, t in headings if l == 2],
        "out_links_raw": out_links,
        "summary": summary[:400],
        "url_links": [t for _l, t in md_links if t.startswith("http")],
    }


# --------------------------------------------------------------------------- #
#  Resolve a raw link target to an absolute repo-relative path
# --------------------------------------------------------------------------- #
def resolve_link(src_path_rel: str, target: str, known: dict) -> str | None:
    if not target:
        return None
    src_dir = os.path.dirname(src_path_rel)
    # direct relative resolution
    candidate = os.path.normpath(os.path.join(src_dir, target)).replace("\\", "/")
    if candidate in known:
        return candidate
    # try adding .md
    if candidate + ".md" in known:
        return candidate + ".md"
    # try index inside a folder link
    idx = (candidate.rstrip("/") + "/00-Index.md")
    if idx in known:
        return idx
    # wikilink by title/stem
    stem = os.path.splitext(os.path.basename(target))[0]
    for k in known:
        if Path(k).stem == stem:
            return k
    return None


# --------------------------------------------------------------------------- #
#  Walk the repository
# --------------------------------------------------------------------------- #
MAX_FILE_BYTES = 8 * 1024 * 1024          # never choke on a giant/binary file
CODE_EXT = {".cpp", ".cc", ".c", ".h", ".hpp", ".py", ".java", ".js", ".jsx",
            ".ts", ".tsx", ".go", ".rs", ".kt", ".rb", ".sql"}


def walk_repo() -> tuple[list[dict], list[dict]]:
    """Return (markdown_atoms, code_atoms). Robust: a single bad file is skipped,
    logged, and never aborts the build."""
    atoms, code_atoms, errors = [], [], []
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for fn in files:
            if fn in IGNORE_FILES:
                continue
            p = Path(root) / fn
            ext = p.suffix.lower()
            try:
                if p.stat().st_size > MAX_FILE_BYTES:
                    errors.append(f"{rel(p)} (skipped: >{MAX_FILE_BYTES} bytes)")
                    continue
                if ext == ".md":
                    atoms.append(parse_markdown(p))
                elif ext in CODE_EXT:
                    code_atoms.append(parse_code(p))
            except Exception as e:                      # noqa: BLE001
                errors.append(f"{rel(p)} ({type(e).__name__}: {e})")
    atoms.sort(key=lambda a: a["path"])
    code_atoms.sort(key=lambda a: a["path"])
    if errors:
        (BRAIN / "_scan-errors.log").write_text(
            f"# scan skipped/failed {len(errors)} files @ {NOW}\n" +
            "\n".join(errors), encoding="utf-8")
        print(f"[warn] {len(errors)} files skipped (see .second-brain/_scan-errors.log)")
    return atoms, code_atoms


def parse_code(path: Path) -> dict:
    """Extract lightweight symbol signatures from a code file."""
    text = path.read_text(encoding="utf-8", errors="replace")
    path_rel = rel(path)
    codex, section = domain_of(path_rel)
    sym_patterns = [
        r"^\s*(?:public|private|protected|static|final|\s)*(?:class|struct|interface|enum)\s+(\w+)",
        r"^\s*def\s+(\w+)\s*\(",
        r"^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(",
        r"^\s*(?:template\s*<[^>]*>\s*)?[\w:<>*&\s]+?\b(\w+)\s*\([^;{]*\)\s*\{",
        r"^\s*(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\(",
        r"^\s*(?:pub\s+)?fn\s+(\w+)\s*\(",
        r"^\s*func\s+(?:\([^)]*\)\s*)?(\w+)\s*\(",
    ]
    symbols = []
    for ln in text.splitlines():
        for pat in sym_patterns:
            m = re.match(pat, ln)
            if m and m.group(1) not in ("if", "for", "while", "switch", "catch"):
                symbols.append(m.group(1))
                break
    symbols = sorted(set(symbols))
    return {
        "id": "code:" + hashlib.sha1(path_rel.encode()).hexdigest()[:12],
        "path": path_rel, "title": path.name, "lang": path.suffix.lstrip("."),
        "codex": codex, "section": section,
        "lines": text.count("\n") + 1, "symbols": symbols[:200],
    }


# --------------------------------------------------------------------------- #
#  Build all artifacts
# --------------------------------------------------------------------------- #
def build():
    for d in (GRAPH_DIR, MEM_DIR, RAG_DIR, OBS_MOC_DIR, KIRO_STEERING, OBSIDIAN_CFG):
        d.mkdir(parents=True, exist_ok=True)

    atoms, code_atoms = walk_repo()
    known = {a["path"]: a for a in atoms}
    print(f"[scan] {len(atoms)} markdown atoms + {len(code_atoms)} code atoms found")

    # ---- resolve links into edges ----------------------------------------- #
    for a in atoms:
        resolved = []
        for t in a["out_links_raw"]:
            r = resolve_link(a["path"], t, known)
            if r and r != a["path"]:
                resolved.append(r)
        a["links"] = sorted(set(resolved))

    codices = {}
    sections = {}
    for a in atoms:
        codices.setdefault(a["codex"], []).append(a["path"])
        sections.setdefault((a["codex"], a["section"]), []).append(a["path"])

    write_manifest(atoms, codices, sections)
    write_graph(atoms, codices, sections)
    write_graph_html()
    write_mermaid(codices, sections)
    write_memories(atoms)
    write_rag(atoms)
    write_rag_tools()
    write_mem0_tool()
    write_obsidian_config()
    write_mocs(atoms, codices, sections)
    write_kiro_steering(atoms, codices, sections)
    write_mcp_example()

    # ---- v2: maximum-recall layers --------------------------------------- #
    concepts = build_concepts(atoms)
    write_concepts(concepts, atoms)
    write_outline(atoms, codices, sections)
    write_summaries(atoms, codices, sections)
    write_communities(atoms)
    write_inverted_index(atoms)
    write_flashcards(atoms, concepts)
    write_coverage_report(atoms, codices, sections)
    write_sqlite_db(atoms, concepts)
    write_llms_txt(atoms, codices, sections)
    write_agents_md(atoms, codices, sections)

    # ---- v3: deeper layers + robustness ---------------------------------- #
    write_code_index(code_atoms)
    write_tfidf(atoms)
    write_triples(atoms, concepts)
    write_bridges(atoms, concepts)
    write_context_pack(atoms, codices, sections, concepts)
    write_finetune_dataset(atoms)
    write_schemas()
    write_editor_tasks()
    write_broken_links(atoms)
    write_history(atoms, code_atoms, codices, sections)
    write_cache(atoms, code_atoms)
    write_brain_cli()

    write_brain_readme(atoms, codices, sections)
    validate_build(atoms)
    print("[done] second brain fully generated.")


# --------------------------------------------------------------------------- #
def write_manifest(atoms, codices, sections):
    total_words = sum(a["words"] for a in atoms)
    manifest = {
        "generated_at": NOW,
        "repo_root": str(REPO_ROOT),
        "stats": {
            "documents": len(atoms),
            "codices": len(codices),
            "sections": len(sections),
            "total_words": total_words,
            "total_edges": sum(len(a["links"]) for a in atoms),
        },
        "codices": {c: len(v) for c, v in sorted(codices.items())},
        "documents": [
            {
                "id": a["id"],
                "path": a["path"],
                "title": a["title"],
                "codex": a["codex"],
                "section": a["section"],
                "words": a["words"],
                "topics": a["h2"][:20],
                "links": a["links"],
                "summary": a["summary"],
            }
            for a in atoms
        ],
    }
    (BRAIN / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print("[write] manifest.json")


# --------------------------------------------------------------------------- #
def write_graph(atoms, codices, sections):
    nodes = []
    edges = []

    # codex nodes
    for c in sorted(codices):
        nodes.append({"id": f"codex:{c}", "label": c, "type": "codex",
                      "group": c, "size": 40})
    # section nodes + hierarchy edges
    seen_sections = set()
    for (c, s), paths in sections.items():
        sid = f"section:{c}/{s}"
        if sid not in seen_sections:
            nodes.append({"id": sid, "label": s, "type": "section",
                          "group": c, "size": 22})
            edges.append({"source": f"codex:{c}", "target": sid,
                          "type": "contains"})
            seen_sections.add(sid)
    # document nodes + hierarchy edges
    for a in atoms:
        nodes.append({
            "id": a["id"], "label": a["title"], "type": "document",
            "group": a["codex"], "path": a["path"], "words": a["words"],
            "size": 10,
        })
        edges.append({"source": f"section:{a['codex']}/{a['section']}",
                      "target": a["id"], "type": "contains"})
    # link edges (document -> document)
    id_by_path = {a["path"]: a["id"] for a in atoms}
    for a in atoms:
        for tgt in a["links"]:
            if tgt in id_by_path:
                edges.append({"source": a["id"], "target": id_by_path[tgt],
                              "type": "links"})

    graph = {"generated_at": NOW, "directed": True,
             "nodes": nodes, "edges": edges,
             "stats": {"nodes": len(nodes), "edges": len(edges)}}
    (GRAPH_DIR / "knowledge-graph.json").write_text(
        json.dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[write] graph/knowledge-graph.json ({len(nodes)} nodes, {len(edges)} edges)")


# --------------------------------------------------------------------------- #
def write_graph_html():
    html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Second Brain · Knowledge Graph</title>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<script src="https://unpkg.com/vis-network@9.1.9/standalone/umd/vis-network.min.js"></script>
<style>
  html,body{margin:0;height:100%;background:#0d1117;color:#e6edf3;font-family:system-ui,sans-serif}
  #bar{position:fixed;top:0;left:0;right:0;padding:10px 14px;background:#161b22;
       border-bottom:1px solid #30363d;z-index:10;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
  #bar h1{font-size:15px;margin:0;font-weight:600}
  #bar input{background:#0d1117;border:1px solid #30363d;color:#e6edf3;padding:6px 10px;border-radius:6px;width:260px}
  #bar span{color:#7d8590;font-size:12px}
  #net{position:absolute;top:52px;bottom:0;left:0;right:0}
  #info{position:fixed;bottom:14px;right:14px;max-width:340px;background:#161b22;
        border:1px solid #30363d;border-radius:8px;padding:12px;font-size:13px;display:none}
  a{color:#58a6ff}
</style>
</head>
<body>
<div id="bar">
  <h1>🧠 Second Brain — Knowledge Graph</h1>
  <input id="q" placeholder="search & focus a node…"/>
  <span id="stats"></span>
</div>
<div id="net"></div>
<div id="info"></div>
<script>
fetch('knowledge-graph.json').then(r=>r.json()).then(g=>{
  document.getElementById('stats').textContent =
    g.stats.nodes+' nodes · '+g.stats.edges+' edges';
  const palette={};let hue=0;
  function color(grp){if(!palette[grp]){palette[grp]='hsl('+(hue=(hue+47)%360)+',65%,55%)';}return palette[grp];}
  const nodes=new vis.DataSet(g.nodes.map(n=>({
    id:n.id,label:n.label,value:n.size,group:n.group,
    color:{background:color(n.group),border:'#0d1117'},
    font:{color:'#e6edf3',size:n.type==='codex'?20:(n.type==='section'?14:11)},
    shape:n.type==='document'?'dot':'box',path:n.path
  })));
  const edges=new vis.DataSet(g.edges.map(e=>({
    from:e.source,to:e.target,
    color:{color:e.type==='links'?'#3fb950':'#30363d',opacity:e.type==='links'?0.7:0.35},
    dashes:e.type==='links',arrows:e.type==='links'?'to':undefined
  })));
  const net=new vis.Network(document.getElementById('net'),{nodes,edges},{
    physics:{stabilization:true,barnesHut:{gravitationalConstant:-8000,springLength:120}},
    interaction:{hover:true,tooltipDelay:120}
  });
  const info=document.getElementById('info');
  net.on('click',p=>{
    if(!p.nodes.length){info.style.display='none';return;}
    const n=nodes.get(p.nodes[0]);
    info.style.display='block';
    info.innerHTML='<b>'+n.label+'</b><br><span style="color:#7d8590">'+(n.group||'')+'</span>'+
      (n.path?'<br><br><code>'+n.path+'</code>':'');
  });
  document.getElementById('q').addEventListener('input',e=>{
    const term=e.target.value.toLowerCase();if(!term)return;
    const hit=g.nodes.find(n=>n.label.toLowerCase().includes(term));
    if(hit){net.focus(hit.id,{scale:1.2,animation:true});net.selectNodes([hit.id]);}
  });
});
</script>
</body>
</html>
"""
    (GRAPH_DIR / "graph.html").write_text(html, encoding="utf-8")
    print("[write] graph/graph.html")


# --------------------------------------------------------------------------- #
def write_mermaid(codices, sections):
    lines = ["```mermaid", "graph TD"]
    lines.append('  ROOT["🧠 Second Brain"]')
    for c in sorted(codices):
        cid = "C_" + slug(c).replace("-", "_")
        lines.append(f'  ROOT --> {cid}["{c}<br/>({len(codices[c])} docs)"]')
        secs = sorted({s for (cc, s) in sections if cc == c})
        for s in secs:
            sid = cid + "_" + slug(s).replace("-", "_")
            n = len(sections[(c, s)])
            lines.append(f'  {cid} --> {sid}["{s}<br/>({n})"]')
    lines.append("```")
    (GRAPH_DIR / "graph.mermaid").write_text("\n".join(lines), encoding="utf-8")
    print("[write] graph/graph.mermaid")


# --------------------------------------------------------------------------- #
def write_memories(atoms):
    """mem0-style atomic memories. One JSON object per line."""
    out = []
    for a in atoms:
        topic_str = "; ".join(a["h2"][:12])
        mem_text = (
            f"In the '{a['codex']}' codex, section '{a['section']}', the document "
            f"'{a['title']}' ({a['path']}) covers: {topic_str or a['summary']}."
        )
        out.append({
            "memory": mem_text,
            "metadata": {
                "source": a["path"],
                "title": a["title"],
                "codex": a["codex"],
                "section": a["section"],
                "type": "document-summary",
                "topics": a["h2"][:20],
                "doc_id": a["id"],
            },
        })
        # per-topic memories for the richest recall
        for h in a["h2"][:25]:
            out.append({
                "memory": f"'{a['title']}' ({a['path']}) explains: {h}.",
                "metadata": {
                    "source": a["path"], "title": a["title"],
                    "codex": a["codex"], "section": a["section"],
                    "type": "topic", "topic": h, "doc_id": a["id"],
                },
            })
    with (MEM_DIR / "memories.jsonl").open("w", encoding="utf-8") as f:
        for rec in out:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"[write] memory/memories.jsonl ({len(out)} memories)")


# --------------------------------------------------------------------------- #
def chunk_text(text: str, max_chars: int = 1400, overlap: int = 200):
    """Split on headings first, then hard-wrap long sections."""
    blocks = re.split(r"(?=^#{1,6}\s)", text, flags=re.MULTILINE)
    chunks = []
    for b in blocks:
        b = b.strip()
        if not b:
            continue
        if len(b) <= max_chars:
            chunks.append(b)
        else:
            i = 0
            while i < len(b):
                chunks.append(b[i:i + max_chars])
                i += max_chars - overlap
    return chunks


def write_rag(atoms):
    count = 0
    with (RAG_DIR / "chunks.jsonl").open("w", encoding="utf-8") as f:
        for a in atoms:
            p = REPO_ROOT / a["path"]
            text = p.read_text(encoding="utf-8", errors="replace")
            for i, ch in enumerate(chunk_text(text)):
                rec = {
                    "id": f"{a['id']}::{i}",
                    "doc_id": a["id"],
                    "path": a["path"],
                    "title": a["title"],
                    "codex": a["codex"],
                    "section": a["section"],
                    "chunk_index": i,
                    "text": ch,
                }
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                count += 1
    print(f"[write] rag/chunks.jsonl ({count} chunks)")


# --------------------------------------------------------------------------- #
def write_rag_tools():
    build_py = r'''#!/usr/bin/env python3
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
'''
    (RAG_DIR / "build_index.py").write_text(build_py, encoding="utf-8")

    query_py = r'''#!/usr/bin/env python3
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
'''
    (RAG_DIR / "query.py").write_text(query_py, encoding="utf-8")
    print("[write] rag/build_index.py, rag/query.py")


# --------------------------------------------------------------------------- #
def write_mem0_tool():
    ingest = r'''#!/usr/bin/env python3
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
'''
    (MEM_DIR / "mem0_ingest.py").write_text(ingest, encoding="utf-8")

    readme = """# 🧠 Memory Layer (mem0)

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
"""
    (MEM_DIR / "README.md").write_text(readme, encoding="utf-8")
    print("[write] memory/mem0_ingest.py, memory/README.md")


# --------------------------------------------------------------------------- #
def write_obsidian_config():
    app = {
        "alwaysUpdateLinks": True,
        "newLinkFormat": "shortest",
        "useMarkdownLinks": False,
        "attachmentFolderPath": ".attachments",
        "showLineNumber": True,
    }
    (OBSIDIAN_CFG / "app.json").write_text(
        json.dumps(app, indent=2), encoding="utf-8")

    graph_cfg = {
        "collapse-filter": True,
        "search": "",
        "showTags": True,
        "showAttachments": False,
        "hideUnresolved": False,
        "showOrphans": True,
        "collapse-color-groups": False,
        "colorGroups": [
            {"query": "path:DSA-Grandmaster-Codex", "color": {"a": 1, "rgb": 5431378}},
            {"query": "path:FULLSTACK-AI-GRANDMASTER-CODEX", "color": {"a": 1, "rgb": 3908005}},
            {"query": "path:.second-brain", "color": {"a": 1, "rgb": 14701138}},
        ],
        "collapse-display": True,
        "showArrow": True,
        "textFadeMultiplier": 0,
        "nodeSizeMultiplier": 1.3,
        "lineSizeMultiplier": 1,
        "collapse-forces": True,
        "centerStrength": 0.5,
        "repelStrength": 12,
        "linkStrength": 1,
        "linkDistance": 250,
        "scale": 1,
    }
    (OBSIDIAN_CFG / "graph.json").write_text(
        json.dumps(graph_cfg, indent=2), encoding="utf-8")

    core = ["file-explorer", "global-search", "switcher", "graph", "backlink",
            "outgoing-link", "tag-pane", "page-preview", "note-composer",
            "command-palette", "outline", "word-count", "file-recovery"]
    (OBSIDIAN_CFG / "core-plugins.json").write_text(
        json.dumps(core, indent=2), encoding="utf-8")
    print("[write] .obsidian/ vault config")


# --------------------------------------------------------------------------- #
def write_mocs(atoms, codices, sections):
    """Obsidian Maps-of-Content: wikilink hubs per codex + section."""
    # self-heal: remove stale MOCs (e.g., from a deleted codex) before regenerating
    for old in OBS_MOC_DIR.glob("MOC-*.md"):
        old.unlink()
    # master MOC
    lines = ["---", "tags: [MOC, second-brain, root]", "---",
             "# 🧠 Master Map of Content", "",
             "The single entry point. Every codex, section, and document is",
             "reachable from here through backlinks.", ""]
    for c in sorted(codices):
        lines.append(f"## {c}  ·  {len(codices[c])} documents")
        lines.append(f"- [[MOC-{slug(c)}|Open {c} map]]")
        lines.append("")
    (OBS_MOC_DIR / "MOC-Master.md").write_text("\n".join(lines), encoding="utf-8")

    # per-codex MOC
    def obs_link(path_rel):
        # Obsidian shortest-link uses the file stem
        return Path(path_rel).stem

    for c in sorted(codices):
        lines = ["---", f"tags: [MOC, {slug(c)}]", "---",
                 f"# 🗺️ {c} — Map of Content", "",
                 "[[MOC-Master|← Master Map]]", ""]
        secs = sorted({s for (cc, s) in sections if cc == c})
        for s in secs:
            lines.append(f"## {s}")
            for p in sorted(sections[(c, s)]):
                a = next(x for x in atoms if x["path"] == p)
                lines.append(f"- [[{obs_link(p)}|{a['title']}]]")
            lines.append("")
        (OBS_MOC_DIR / f"MOC-{slug(c)}.md").write_text(
            "\n".join(lines), encoding="utf-8")
    print(f"[write] obsidian/MOCs/ ({len(codices)+1} maps)")


# --------------------------------------------------------------------------- #
def write_kiro_steering(atoms, codices, sections):
    """The always-injected memory that makes the Kiro AI never forget."""
    total_words = sum(a["words"] for a in atoms)
    codex_rows = "\n".join(
        f"| `{c}` | {len(v)} | {', '.join(sorted({s for (cc, s) in sections if cc == c}))[:120]} |"
        for c, v in sorted(codices.items()))

    steering = f"""---
inclusion: always
---
# 🧠 SECOND BRAIN — Permanent Memory (auto-generated, do not hand-edit)

> This file is injected into every conversation. It is my persistent memory of
> the **{PROJECT_NAME}** knowledge base in this workspace. When the user refers to
> "the system", "the engine", "the codex", or "the OS", they mean this.

## What exists here
- **{len(atoms)} documents**, **{total_words:,} words**, across **{len(codices)} codices** and **{len(sections)} sections**.
- Full machine index: `.second-brain/manifest.json`
- Knowledge graph: `.second-brain/graph/knowledge-graph.json` (+ `graph.html` viewer)
- Long-term memory: `.second-brain/memory/memories.jsonl` (mem0-ready)
- Semantic retrieval (RAG): `.second-brain/rag/` (`build_index.py`, `query.py`)
- Obsidian vault: repo root is the vault; hubs in `.second-brain/obsidian/MOCs/`

## The codices
| Codex | Docs | Sections (partial) |
|-------|-----:|--------------------|
{codex_rows}

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
   (or keep `python .second-brain/watch_and_build.py` running to auto-rebuild on save).
5. **If anything seems off**, run `brain.py doctor` — it self-validates every artifact.
6. Treat `manifest.json` + graph + `tfidf-model.json` as the source of truth.

## Regeneration contract
This second brain is generated. If content drifts, rerun the generator. Do not
manually edit generated files under `.second-brain/` (except the generator and
the human READMEs).
"""
    (KIRO_STEERING / "second-brain.md").write_text(steering, encoding="utf-8")

    # a lean navigation cheat-sheet (also always-on)
    nav_lines = ["---", "inclusion: always", "---",
                 "# 🗺️ Codex Navigation Cheat-Sheet (auto-generated)", "",
                 "Top-level sections, so I can route any request instantly.", ""]
    for c in sorted(codices):
        nav_lines.append(f"## {c}")
        for s in sorted({s for (cc, s) in sections if cc == c}):
            first = sorted(sections[(c, s)])[0]
            nav_lines.append(f"- **{s}** → e.g. `{first}`")
        nav_lines.append("")
    (KIRO_STEERING / "codex-navigation.md").write_text(
        "\n".join(nav_lines), encoding="utf-8")
    print("[write] .kiro/steering/second-brain.md, codex-navigation.md")


# --------------------------------------------------------------------------- #
def write_mcp_example():
    cfg = {
        "mcpServers": {
            "second-brain-memory": {
                "command": "uvx",
                "args": ["mem0-mcp@latest"],
                "env": {
                    "MEM0_API_KEY": "<optional-for-hosted-mem0>",
                    "FASTMCP_LOG_LEVEL": "ERROR"
                },
                "disabled": False,
                "autoApprove": ["search_memory", "list_memories"]
            }
        }
    }
    note = (
        "// Example Kiro MCP config to plug the second brain's memory into any\n"
        "// agent session. Copy the 'second-brain-memory' block into your real\n"
        "// .kiro/settings/mcp.json (workspace) or ~/.kiro/settings/mcp.json (user).\n"
        "// After ingesting memories via memory/mem0_ingest.py, the agent can\n"
        "// search the codex memory through MCP tools.\n"
    )
    (BRAIN / "mcp").mkdir(exist_ok=True)
    (BRAIN / "mcp" / "mcp.example.json").write_text(
        note + json.dumps(cfg, indent=2), encoding="utf-8")
    print("[write] mcp/mcp.example.json")


# --------------------------------------------------------------------------- #
def write_brain_readme(atoms, codices, sections):
    total_words = sum(a["words"] for a in atoms)
    edges = sum(len(a["links"]) for a in atoms)
    readme = f"""# 🧠 THE SECOND BRAIN — {PROJECT_NAME}

A complete, portable, always-on memory system for this project. Built so **any AI
(and you) can remember everything, forever, with no context-window limit** —
through graph navigation, long-term memory, and semantic retrieval.

> Generated by `build_second_brain.py`. Rerun it any time the codex changes:
> ```bash
> python .second-brain/build_second_brain.py
> ```

## 📊 What it indexes right now
- **{len(atoms)} documents** · **{total_words:,} words**
- **{len(codices)} codices** · **{len(sections)} sections** · **{edges} internal links**

## 🧩 The layers
| Layer | Location | What it gives you |
|-------|----------|-------------------|
| **Inventory** | `manifest.json` | Every doc: title, path, topics, links, summary |
| **Graphify** | `graph/knowledge-graph.json`, `graph.html`, `graph.mermaid` | Nodes + edges; open `graph.html` in a browser |
| **GraphRAG communities** | `graph/communities.json` | Linked-document clusters + themed summaries |
| **Mem0** | `memory/memories.jsonl`, `memory/mem0_ingest.py` | Atomic long-term memories for any agent |
| **RAG (semantic)** | `rag/chunks.jsonl`, `rag/build_index.py`, `rag/query.py` | Vector search = no context limit |
| **SQLite + FTS5** | `brain.db` | Instant full-text search, zero external deps |
| **Zero-dep CLI** | `brain.py` | `search / find / related / concept / outline / summary / stats / gaps` |
| **Concepts / glossary** | `concepts.json`, `glossary.md` | Every concept → the docs that define it |
| **Global outline** | `outline.md`, `outline.json` | The full heading tree of the whole corpus |
| **Hierarchical summaries** | `summaries.md`, `summaries.json` | RAPTOR-style doc→section→codex roll-ups |
| **Inverted index** | `inverted-index.json` | Offline keyword → docs, no DB needed |
| **Flashcards** | `flashcards.jsonl`, `flashcards-anki.csv` | Spaced-repetition + AI self-eval Q&A |
| **Coverage/gaps** | `coverage-report.md` | Orphans, stubs, missing indexes, TODOs |
| **llms.txt standard** | `../llms.txt`, `llms-full.txt` | AI-agent corpus map (llmstxt.org spec) |
| **AGENTS.md** | `../AGENTS.md`, `../CLAUDE.md` | Universal agent onboarding instructions |
| **Obsidian** | `.obsidian/` (repo = vault), `obsidian/MOCs/` | Visual graph + Maps-of-Content |
| **Kiro memory** | `.kiro/steering/second-brain.md` | Always injected into my (the AI's) context |
| **MCP** | `mcp/mcp.example.json` | Plug memory into any MCP-aware agent |

## 🚀 Quick start
```bash
# 1. (Re)build the whole second brain from the live repo
python .second-brain/build_second_brain.py

# 2. Explore the graph — just open in a browser
#    .second-brain/graph/graph.html

# 3. Enable semantic recall (optional, needs deps)
pip install chromadb sentence-transformers
python .second-brain/rag/build_index.py
python .second-brain/rag/query.py "how does Dijkstra relate to BFS"

# 4. Load long-term memory into mem0 (optional, needs deps)
pip install mem0ai
python .second-brain/memory/mem0_ingest.py

# 5. Open the repo folder in Obsidian → the graph + MOCs light up
```

## 🔁 Keeping it alive
The second brain is a **projection** of the codices, not a copy to maintain by
hand. Whenever you add or edit codex files, rerun the generator — or keep
`python .second-brain/watch_and_build.py` running to auto-rebuild on every save.
(A Kiro `fileEdited` hook is intentionally avoided: it opens a new tab/history
entry per run and floods the workspace.)

## 🗂️ Codices
{chr(10).join(f"- **{c}** — {len(v)} docs" for c, v in sorted(codices.items()))}
"""
    (BRAIN / "README.md").write_text(readme, encoding="utf-8")
    print("[write] README.md")


# --------------------------------------------------------------------------- #
#  v2 MAXIMUM-RECALL LAYERS  (appended below, __main__ at very end)
# --------------------------------------------------------------------------- #

EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\u2600-\u27BF\u2190-\u21FF\u2B00-\u2BFF\uFE0F\u200d]")
ENUM_RE = re.compile(r"^\s*(?:[IVXLCDM]+[\.\)]|\d+[\.\)]|[A-Za-z][\.\)])\s*")
STOPWORDS = set("""a an the of to in on at for and or but is are was were be been being
this that these those it its as by with from into out up down off over under again
how what why when where which who whom your you i we they he she them his her our their
not no nor do does did done has have had can could should would may might must will
just also very more most much many few some any all each every both other than then
one two three first second use used using via etc eg ie vs """.split())


BOILERPLATE = {
    "contents", "common pitfalls", "common pitfalls / gotchas",
    "common pitfalls & gotchas", "common pitfalls — a checklist", "key takeaways",
    "how to use", "how to use this codex", "recommended learning order",
    "why it's worth it", "the critical rule", "prevention", "what this is",
    "the great map", "the foundational mantras", "decision guide", "why this order",
    "related sections", "deep references", "deep references (authoritative sources)",
    "setup", "how to study this section", "suggested cadence", "prerequisites",
    "begin", "the big picture", "what you'll be able to do", "quick start",
    "overview", "summary", "introduction", "conclusion", "references", "resources",
    "what you will own after this section", "contents (learning order)",
    "contents — learning order", "the 60-second answer", "notes", "example",
    "examples", "why", "what", "how", "goal", "goals", "index", "table of contents",
}


def norm_concept(h: str) -> str:
    h = EMOJI_RE.sub("", h)
    h = ENUM_RE.sub("", h)
    h = re.sub(r"\s+", " ", h).strip(" -—:·")
    return h.strip()


def is_boilerplate(concept: str) -> bool:
    c = concept.lower().strip()
    if c in BOILERPLATE:
        return True
    # generic multi-word headers that start with these are structural
    for pre in ("complete ", "what you will", "what you'll", "how to study",
                "contents", "recommended "):
        if c.startswith(pre):
            return True
    return False


def tokenize(text: str):
    for w in re.findall(r"[A-Za-z][A-Za-z0-9+#\-]{1,}", text.lower()):
        if w not in STOPWORDS and len(w) > 2:
            yield w


# --------------------------------------------------------------------------- #
def build_concepts(atoms) -> dict:
    """Concept index: normalized heading/title -> docs that teach it."""
    concepts = {}
    for a in atoms:
        seeds = [(a["title"], True)] + [(h["text"], False) for h in a["headings"]
                                        if h["level"] in (2, 3)]
        for raw, is_title in seeds:
            c = norm_concept(raw)
            if len(c) < 3 or len(c) > 80 or is_boilerplate(c):
                continue
            key = c.lower()
            rec = concepts.setdefault(key, {"concept": c, "docs": [], "defining": []})
            if a["path"] not in rec["docs"]:
                rec["docs"].append(a["path"])
            if is_title and a["path"] not in rec["defining"]:
                rec["defining"].append(a["path"])
    return concepts


def write_concepts(concepts, atoms):
    ranked = sorted(concepts.values(), key=lambda r: (-len(r["docs"]), r["concept"]))
    (BRAIN / "concepts.json").write_text(
        json.dumps({"generated_at": NOW, "count": len(ranked), "concepts": ranked},
                   indent=2, ensure_ascii=False), encoding="utf-8")

    lines = ["# 📖 Glossary & Concept Index (auto-generated)", "",
             f"{len(ranked)} concepts extracted from titles and section headings.",
             "Each links to the documents that define or teach it.", ""]
    for r in ranked:
        if len(r["docs"]) < 1:
            continue
        defn = r["defining"] or r["docs"][:1]
        anchor = ", ".join(f"`{d}`" for d in defn[:3])
        extra = f" (+{len(r['docs'])-len(defn)} more)" if len(r["docs"]) > len(defn) else ""
        lines.append(f"- **{r['concept']}** — {anchor}{extra}")
    (BRAIN / "glossary.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"[write] concepts.json, glossary.md ({len(ranked)} concepts)")


# --------------------------------------------------------------------------- #
def write_outline(atoms, codices, sections):
    """Global outline: the entire heading tree of every document (RAPTOR base)."""
    data = {"generated_at": NOW, "codices": {}}
    md = ["# 🌳 Global Outline — the full shape of the codex (auto-generated)", ""]
    for c in sorted(codices):
        md.append(f"# {c}")
        data["codices"][c] = {}
        for s in sorted({s for (cc, s) in sections if cc == c}):
            md.append(f"\n## {s}")
            data["codices"][c][s] = []
            for p in sorted(sections[(c, s)]):
                a = next(x for x in atoms if x["path"] == p)
                md.append(f"\n### {a['title']}  · `{p}`")
                topics = a["h2"][:30]
                data["codices"][c][s].append(
                    {"path": p, "title": a["title"], "topics": topics})
                for t in topics:
                    md.append(f"- {norm_concept(t)}")
    (BRAIN / "outline.md").write_text("\n".join(md), encoding="utf-8")
    (BRAIN / "outline.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print("[write] outline.md, outline.json")


# --------------------------------------------------------------------------- #
def write_summaries(atoms, codices, sections):
    """RAPTOR-style hierarchical summary tree: doc -> section -> codex."""
    tree = {"generated_at": NOW, "codices": {}}
    md = ["# 🧾 Hierarchical Summaries (auto-generated)",
          "", "Rolled up doc → section → codex, so an agent can read the whole",
          "codex at any zoom level without loading full text.", ""]
    for c in sorted(codices):
        secs = sorted({s for (cc, s) in sections if cc == c})
        cnode = {"documents": len(codices[c]), "sections": {}}
        md.append(f"\n## {c}  ·  {len(codices[c])} docs · {len(secs)} sections")
        for s in secs:
            paths = sorted(sections[(c, s)])
            topic_freq = {}
            titles = []
            for p in paths:
                a = next(x for x in atoms if x["path"] == p)
                titles.append(a["title"])
                for t in a["h2"]:
                    k = norm_concept(t).lower()
                    if k and not is_boilerplate(k):
                        topic_freq[k] = topic_freq.get(k, 0) + 1
            top = [t for t, _ in sorted(topic_freq.items(),
                                        key=lambda kv: -kv[1])[:12]]
            summary = (f"{len(paths)} documents covering: " + ", ".join(top[:12])
                       + ".") if top else f"{len(paths)} documents."
            cnode["sections"][s] = {"documents": len(paths),
                                    "titles": titles, "key_topics": top,
                                    "summary": summary}
            md.append(f"\n### {s}\n{summary}")
        tree["codices"][c] = cnode
    (BRAIN / "summaries.json").write_text(
        json.dumps(tree, indent=2, ensure_ascii=False), encoding="utf-8")
    (BRAIN / "summaries.md").write_text("\n".join(md), encoding="utf-8")
    print("[write] summaries.json, summaries.md")


# --------------------------------------------------------------------------- #
def write_communities(atoms):
    """GraphRAG-style communities via connected components of the link graph."""
    id_by_path = {a["path"]: a["id"] for a in atoms}
    by_id = {a["id"]: a for a in atoms}
    adj = {a["id"]: set() for a in atoms}
    for a in atoms:
        for t in a["links"]:
            if t in id_by_path:
                adj[a["id"]].add(id_by_path[t])
                adj[id_by_path[t]].add(a["id"])

    seen, comps = set(), []
    for nid in adj:
        if nid in seen:
            continue
        stack, comp = [nid], []
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            comp.append(x)
            stack.extend(adj[x] - seen)
        comps.append(comp)

    communities = []
    for i, comp in enumerate(sorted(comps, key=len, reverse=True)):
        members = [by_id[x] for x in comp]
        topic_freq = {}
        for m in members:
            for t in m["h2"]:
                k = norm_concept(t).lower()
                if k and not is_boilerplate(k):
                    topic_freq[k] = topic_freq.get(k, 0) + 1
        top = [t for t, _ in sorted(topic_freq.items(), key=lambda kv: -kv[1])[:10]]
        communities.append({
            "id": f"community:{i}",
            "size": len(members),
            "codices": sorted({m["codex"] for m in members}),
            "members": [m["path"] for m in members[:60]],
            "key_topics": top,
            "summary": (f"Cluster of {len(members)} linked documents across "
                        f"{', '.join(sorted({m['codex'] for m in members}))}; "
                        f"themes: {', '.join(top[:8])}."),
        })
    (BRAIN / "graph" / "communities.json").write_text(
        json.dumps({"generated_at": NOW, "count": len(communities),
                    "communities": communities}, indent=2, ensure_ascii=False),
        encoding="utf-8")
    print(f"[write] graph/communities.json ({len(communities)} communities)")


# --------------------------------------------------------------------------- #
def write_inverted_index(atoms):
    """Offline keyword search: term -> [doc paths], stdlib-only fallback search."""
    index = {}
    for a in atoms:
        field = " ".join([a["title"], " ".join(a["h2"]),
                          " ".join(h["text"] for h in a["headings"]),
                          a["summary"]])
        for tok in set(tokenize(field)):
            index.setdefault(tok, [])
            if a["path"] not in index[tok]:
                index[tok].append(a["path"])
    # drop ultra-common tokens (appear in >60% of docs) to keep it useful
    cutoff = max(5, int(0.6 * len(atoms)))
    index = {k: v for k, v in index.items() if len(v) <= cutoff}
    (BRAIN / "inverted-index.json").write_text(
        json.dumps({"generated_at": NOW, "terms": len(index), "index": index},
                   ensure_ascii=False), encoding="utf-8")
    print(f"[write] inverted-index.json ({len(index)} terms)")


# --------------------------------------------------------------------------- #
def write_flashcards(atoms, concepts):
    """Q&A pairs for spaced repetition + AI self-evaluation."""
    cards = []
    for a in atoms:
        if a["h2"]:
            cards.append({
                "q": f"What topics does '{a['title']}' cover, and where does it live?",
                "a": f"{a['path']} — covers: " + "; ".join(a["h2"][:12]),
                "tags": [a["codex"], a["section"]],
            })
    for r in sorted(concepts.values(), key=lambda r: -len(r["docs"]))[:1500]:
        defn = (r["defining"] or r["docs"])[:2]
        cards.append({
            "q": f"Where in the codex is '{r['concept']}' taught?",
            "a": ", ".join(defn),
            "tags": ["concept"],
        })
    with (BRAIN / "flashcards.jsonl").open("w", encoding="utf-8") as f:
        for c in cards:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    # Anki-importable CSV (front,back)
    import csv
    with (BRAIN / "flashcards-anki.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        for c in cards:
            w.writerow([c["q"], c["a"]])
    print(f"[write] flashcards.jsonl, flashcards-anki.csv ({len(cards)} cards)")


# --------------------------------------------------------------------------- #
def write_coverage_report(atoms, codices, sections):
    """Gap analysis: orphans, stubs, missing indexes, TODO markers."""
    id_by_path = {a["path"]: a["id"] for a in atoms}
    indeg = {a["id"]: 0 for a in atoms}
    for a in atoms:
        for t in a["links"]:
            if t in id_by_path:
                indeg[id_by_path[t]] += 1
    orphans = [a["path"] for a in atoms
               if indeg[a["id"]] == 0 and not a["path"].endswith("00-Index.md")
               and "README" not in a["path"] and "INDEX" not in a["path"].upper()]
    stubs = [(a["path"], a["words"]) for a in atoms if a["words"] < 150]
    missing_index = []
    for (c, s) in sections:
        if not any(p.endswith("00-Index.md") for p in sections[(c, s)]):
            missing_index.append(f"{c}/{s}")
    todos = []
    for a in atoms:
        body = (REPO_ROOT / a["path"]).read_text(encoding="utf-8", errors="replace")
        for marker in ("TODO", "FIXME", "PLACEHOLDER", "COMING SOON", "TBD"):
            if marker in body:
                todos.append((a["path"], marker))
                break

    lines = ["# 🩺 Coverage & Gap Report (auto-generated)", "",
             f"- Documents: {len(atoms)}",
             f"- Orphans (no inbound links): {len(orphans)}",
             f"- Stubs (<150 words): {len(stubs)}",
             f"- Sections missing 00-Index.md: {len(missing_index)}",
             f"- Files with TODO/FIXME/TBD markers: {len(todos)}", ""]
    def block(title, items):
        lines.append(f"## {title} ({len(items)})")
        for it in items[:200]:
            lines.append(f"- {it}")
        lines.append("")
    block("Orphan documents", orphans)
    block("Stub documents", [f"{p} ({w} words)" for p, w in sorted(stubs, key=lambda x: x[1])])
    block("Sections missing an index", missing_index)
    block("Documents with unfinished markers", [f"{p} [{m}]" for p, m in todos])
    (BRAIN / "coverage-report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"[write] coverage-report.md (orphans={len(orphans)}, stubs={len(stubs)})")


# --------------------------------------------------------------------------- #
def write_sqlite_db(atoms, concepts):
    """Single queryable DB with FTS5 full-text search over every chunk."""
    import sqlite3
    db_path = BRAIN / "brain.db"
    if db_path.exists():
        db_path.unlink()
    con = sqlite3.connect(str(db_path))
    cur = con.cursor()
    cur.execute("""CREATE TABLE documents(
        id TEXT PRIMARY KEY, path TEXT, title TEXT, codex TEXT,
        section TEXT, words INTEGER, summary TEXT)""")
    cur.execute("""CREATE TABLE links(src TEXT, dst TEXT)""")
    cur.execute("""CREATE TABLE concepts(concept TEXT, path TEXT)""")

    fts_ok = True
    try:
        cur.execute("""CREATE VIRTUAL TABLE chunks USING fts5(
            path, title, codex, section, text)""")
    except sqlite3.OperationalError:
        fts_ok = False
        cur.execute("""CREATE TABLE chunks(
            path TEXT, title TEXT, codex TEXT, section TEXT, text TEXT)""")

    for a in atoms:
        cur.execute("INSERT INTO documents VALUES(?,?,?,?,?,?,?)",
                    (a["id"], a["path"], a["title"], a["codex"],
                     a["section"], a["words"], a["summary"]))
        for t in a["links"]:
            cur.execute("INSERT INTO links VALUES(?,?)", (a["path"], t))
    for r in concepts.values():
        for p in r["docs"]:
            cur.execute("INSERT INTO concepts VALUES(?,?)", (r["concept"], p))

    # load chunks from rag/chunks.jsonl
    n = 0
    with (RAG_DIR / "chunks.jsonl").open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            cur.execute("INSERT INTO chunks VALUES(?,?,?,?,?)",
                        (r["path"], r["title"], r["codex"], r["section"], r["text"]))
            n += 1
    con.commit()
    con.close()
    print(f"[write] brain.db (FTS5={fts_ok}, {n} searchable chunks)")


# --------------------------------------------------------------------------- #
def write_llms_txt(atoms, codices, sections):
    """The llms.txt standard (Jeremy Howard / llmstxt.org): root index for LLMs."""
    L = [f"# {PROJECT_NAME} — Second Brain", "",
         "> A machine-readable memory system over this project's knowledge base.",
         "> This file maps the corpus for LLMs and AI agents.",
         "> Full index: `.second-brain/manifest.json`.", ""]
    for c in sorted(codices):
        L.append(f"## {c}")
        L.append("")
        for s in sorted({s for (cc, s) in sections if cc == c}):
            idx = [p for p in sections[(c, s)] if p.endswith("00-Index.md")]
            target = idx[0] if idx else sorted(sections[(c, s)])[0]
            a = next(x for x in atoms if x["path"] == target)
            desc = (a["summary"][:90] or s).replace("\n", " ")
            L.append(f"- [{s}]({target}): {desc}")
        L.append("")
    L += ["## Second Brain tooling", "",
          "- [Manifest](.second-brain/manifest.json): full inventory of all docs",
          "- [Knowledge graph](.second-brain/graph/knowledge-graph.json): nodes + edges",
          "- [Outline](.second-brain/outline.md): every heading in the corpus",
          "- [Glossary](.second-brain/glossary.md): concept → defining docs",
          "- [Brain CLI](.second-brain/brain.py): offline search/related/outline", ""]
    (REPO_ROOT / "llms.txt").write_text("\n".join(L), encoding="utf-8")

    # llms-full.txt: concatenated corpus for single-fetch ingestion
    with (BRAIN / "llms-full.txt").open("w", encoding="utf-8") as f:
        f.write("# THE GRANDMASTER CODEX — FULL CORPUS\n")
        f.write(f"# {len(atoms)} documents · generated {NOW}\n\n")
        for a in atoms:
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"FILE: {a['path']}\nTITLE: {a['title']}\n")
            f.write("=" * 80 + "\n\n")
            f.write((REPO_ROOT / a["path"]).read_text(encoding="utf-8", errors="replace"))
            f.write("\n")
    print("[write] llms.txt (root), .second-brain/llms-full.txt")


# --------------------------------------------------------------------------- #
def write_agents_md(atoms, codices, sections):
    """AGENTS.md — universal instructions any AI coding agent reads on entry."""
    total_words = sum(a["words"] for a in atoms)
    txt = f"""# AGENTS.md — Instructions for AI Agents

The **{PROJECT_NAME}** repository ({len(atoms)} docs, {total_words:,} words) ships a
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
{chr(10).join(f"- **{c}** — {len(v)} docs" for c, v in sorted(codices.items()))}
"""
    (REPO_ROOT / "AGENTS.md").write_text(txt, encoding="utf-8")
    # mirror for tools that look for CLAUDE.md / .cursorrules pointers
    (REPO_ROOT / "CLAUDE.md").write_text(
        "See [AGENTS.md](AGENTS.md) — this project uses a shared agent memory system.\n",
        encoding="utf-8")
    print("[write] AGENTS.md (root), CLAUDE.md pointer")


# --------------------------------------------------------------------------- #
def write_brain_cli():
    """Zero-dependency CLI so ANY agent can query the brain from the terminal."""
    cli = r'''#!/usr/bin/env python3
"""
brain.py — zero-dependency query engine for the Second Brain.
Uses only the Python standard library. Run from anywhere in the repo.

  python .second-brain/brain.py ask "how does lazy propagation work"  SEMANTIC (TF-IDF, no deps)
  python .second-brain/brain.py search "lazy propagation"     full-text (FTS5)
  python .second-brain/brain.py find "dijkstra"               inverted-index keyword
  python .second-brain/brain.py code "union find"             code-symbol search
  python .second-brain/brain.py related <path>                graph neighbours
  python .second-brain/brain.py triples <path>                facts about a doc
  python .second-brain/brain.py bridges                       cross-codex shared concepts
  python .second-brain/brain.py concept "segment tree"        where a concept lives
  python .second-brain/brain.py outline [codex]               heading tree
  python .second-brain/brain.py summary [codex]               hierarchical summaries
  python .second-brain/brain.py doc <path>                    one doc's metadata
  python .second-brain/brain.py stats                         corpus statistics
  python .second-brain/brain.py gaps                          coverage report
  python .second-brain/brain.py doctor                        health / integrity check
  python .second-brain/brain.py watch                         auto-rebuild on file changes
"""
import sys, json, sqlite3, pathlib, math, re, subprocess, time
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = pathlib.Path(__file__).resolve().parent
def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))

def cmd_search(q, k=8):
    db = HERE / "brain.db"
    if not db.exists():
        return cmd_find(q, k)
    con = sqlite3.connect(str(db)); cur = con.cursor()
    try:
        rows = cur.execute(
            "SELECT path,title,codex,snippet(chunks,4,'>>','<<','…',12) "
            "FROM chunks WHERE chunks MATCH ? ORDER BY rank LIMIT ?",
            (" OR ".join(q.split()), k)).fetchall()
    except sqlite3.OperationalError:
        rows = cur.execute(
            "SELECT path,title,codex,substr(text,1,200) FROM chunks "
            "WHERE text LIKE ? LIMIT ?", (f"%{q}%", k)).fetchall()
    con.close()
    for i,(p,t,c,sn) in enumerate(rows,1):
        print(f"\n#{i} {t}  [{c}]\n   {p}\n   {sn.strip()}")
    if not rows: print("no matches")

def cmd_find(q, k=20):
    idx = load("inverted-index.json")["index"]
    hits = {}
    for tok in q.lower().split():
        for p in idx.get(tok, []):
            hits[p] = hits.get(p,0)+1
    for p,score in sorted(hits.items(), key=lambda x:-x[1])[:k]:
        print(f"  [{score}] {p}")
    if not hits: print("no matches")

def cmd_related(path):
    g = load("graph/knowledge-graph.json")
    idmap = {n["id"]: n for n in g["nodes"]}
    pid = next((n["id"] for n in g["nodes"] if n.get("path")==path), None)
    if not pid: print("path not found"); return
    for e in g["edges"]:
        if e["type"]=="links" and e["source"]==pid:
            print("  → " + idmap[e["target"]].get("path", e["target"]))
        if e["type"]=="links" and e["target"]==pid:
            print("  ← " + idmap[e["source"]].get("path", e["source"]))

def cmd_concept(q):
    for r in load("concepts.json")["concepts"]:
        if q.lower() in r["concept"].lower():
            print(f"\n{r['concept']}  ({len(r['docs'])} docs)")
            for d in (r["defining"] or r["docs"])[:8]:
                print("   " + d)

def cmd_outline(codex=None):
    o = load("outline.json")["codices"]
    for c,secs in o.items():
        if codex and codex.lower() not in c.lower(): continue
        print(f"\n# {c}")
        for s,docs in secs.items():
            print(f"  ## {s}  ({len(docs)})")

def cmd_summary(codex=None):
    s = load("summaries.json")["codices"]
    for c,node in s.items():
        if codex and codex.lower() not in c.lower(): continue
        print(f"\n# {c} — {node['documents']} docs")
        for sec,info in node["sections"].items():
            print(f"  {sec}: {info['summary']}")

def cmd_doc(path):
    for d in load("manifest.json")["documents"]:
        if d["path"]==path or path in d["path"]:
            print(json.dumps(d, indent=2, ensure_ascii=False)); return
    print("not found")

def cmd_stats():
    print(json.dumps(load("manifest.json")["stats"], indent=2))

def cmd_gaps():
    print((HERE / "coverage-report.md").read_text(encoding="utf-8")[:3000])

_STOP = set("the a an of to in on at for and or is are be this that it as by with from".split())
def _tok(s):
    return [w for w in re.findall(r"[A-Za-z][A-Za-z0-9+#\-]{1,}", s.lower())
            if w not in _STOP and len(w) > 2]

def cmd_ask(q, k=8):
    """Dependency-free semantic search via TF-IDF cosine similarity."""
    m = load("tfidf-model.json")
    idf = m["idf"]
    qw = {}
    for t in _tok(q):
        if t in idf:
            qw[t] = qw.get(t, 0) + 1
    if not qw:
        print("no known terms in query; try `search` or `find`"); return
    qv = {t: (1 + math.log(c)) * idf[t] for t, c in qw.items()}
    qn = math.sqrt(sum(v*v for v in qv.values())) or 1.0
    scored = []
    for d in m["docs"]:
        dot = sum(qv.get(t, 0) * w for t, w in d["vec"].items())
        if dot:
            scored.append((dot / qn, d))
    scored.sort(key=lambda x: -x[0])
    for i, (sc, d) in enumerate(scored[:k], 1):
        print(f"#{i} [{sc:.3f}] {d['title']}  [{d['codex']}]\n    {d['path']}")
    if not scored:
        print("no matches")

def cmd_code(q):
    ci = load("code-index.json")
    ql = q.lower()
    for f in ci["files"]:
        hits = [s for s in f["symbols"] if ql in s.lower()]
        if ql in f["path"].lower() or hits:
            print(f"  {f['path']}  ({f['lang']}, {f['lines']} lines)")
            if hits:
                print("      symbols: " + ", ".join(hits[:10]))

def cmd_triples(path):
    t = load("graph/triples.json")["triples"]
    for s, p, o in t:
        if path in s:
            print(f"  {p}: {o}")

def cmd_bridges():
    b = load("bridges.json")["bridges"]
    for r in b[:40]:
        cx = " | ".join(f"{c}: {len(v)}" for c, v in r["codices"].items())
        print(f"  {r['concept']}  ({cx})")

def cmd_doctor():
    rep = load("validation-report.json")
    print("HEALTHY" if rep["healthy"] else "PROBLEMS FOUND")
    for p in rep.get("problems", []):
        print("  ⚠ " + p)
    cov = (HERE / "coverage-report.md").read_text(encoding="utf-8")
    head = "\n".join(cov.splitlines()[:8])
    print("\n" + head)

def cmd_watch(interval=3):
    """Poll for markdown changes and rebuild automatically."""
    root = HERE.parent
    gen = HERE / "build_second_brain.py"
    def snap():
        s = {}
        for p in root.rglob("*.md"):
            if ".git" in p.parts or ".second-brain" in p.parts:
                continue
            try: s[str(p)] = p.stat().st_mtime
            except OSError: pass
        return s
    print("watching for .md changes (Ctrl+C to stop)…")
    last = snap()
    while True:
        time.sleep(interval)
        now = snap()
        if now != last:
            print("change detected → rebuilding")
            subprocess.run([sys.executable, str(gen)])
            last = snap()

def main():
    if len(sys.argv) < 2:
        print(__doc__); return
    cmd, args = sys.argv[1], sys.argv[2:]
    fns = {"ask":lambda:cmd_ask(" ".join(args)),
           "search":lambda:cmd_search(" ".join(args)),
           "find":lambda:cmd_find(" ".join(args)),
           "code":lambda:cmd_code(" ".join(args)),
           "related":lambda:cmd_related(args[0]),
           "triples":lambda:cmd_triples(args[0]),
           "bridges":cmd_bridges,
           "concept":lambda:cmd_concept(" ".join(args)),
           "outline":lambda:cmd_outline(args[0] if args else None),
           "summary":lambda:cmd_summary(args[0] if args else None),
           "doc":lambda:cmd_doc(args[0]),
           "stats":cmd_stats, "gaps":cmd_gaps,
           "doctor":cmd_doctor, "watch":cmd_watch}
    (fns.get(cmd) or (lambda: print(__doc__)))()

if __name__ == "__main__":
    main()
'''
    (BRAIN / "brain.py").write_text(cli, encoding="utf-8")
    print("[write] brain.py (zero-dependency CLI)")


# --------------------------------------------------------------------------- #
#  v3 DEEPER LAYERS + ROBUSTNESS
# --------------------------------------------------------------------------- #
import math


def write_code_index(code_atoms):
    """Index real code (templates, scripts) as first-class knowledge atoms."""
    by_lang = {}
    for c in code_atoms:
        by_lang.setdefault(c["lang"], 0)
        by_lang[c["lang"]] += 1
    data = {"generated_at": NOW, "count": len(code_atoms),
            "by_language": by_lang, "files": code_atoms}
    (BRAIN / "code-index.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[write] code-index.json ({len(code_atoms)} code files, {sum(len(c['symbols']) for c in code_atoms)} symbols)")


# --------------------------------------------------------------------------- #
def write_tfidf(atoms):
    """Dependency-free semantic-ish search: truncated TF-IDF unit vectors.
    Powers `brain.py ask` with NO pip installs required."""
    N = len(atoms)
    df = {}
    doc_tf = []
    for a in atoms:
        try:
            body = (REPO_ROOT / a["path"]).read_text(encoding="utf-8", errors="replace")
        except Exception:
            body = ""
        field = a["title"] + " " + " ".join(a["h2"]) * 3 + " " + body
        tf = {}
        for t in tokenize(field):
            tf[t] = tf.get(t, 0) + 1
        doc_tf.append(tf)
        for t in tf:
            df[t] = df.get(t, 0) + 1

    idf = {t: math.log((N + 1) / (dfi + 1)) + 1 for t, dfi in df.items()}
    docs, keep_terms = [], set()
    for a, tf in zip(atoms, doc_tf):
        weights = {t: (1 + math.log(c)) * idf[t] for t, c in tf.items()}
        top = dict(sorted(weights.items(), key=lambda kv: -kv[1])[:200])
        norm = math.sqrt(sum(w * w for w in top.values())) or 1.0
        unit = {t: round(w / norm, 5) for t, w in top.items()}
        keep_terms.update(unit.keys())
        docs.append({"path": a["path"], "title": a["title"],
                     "codex": a["codex"], "vec": unit})
    model = {"generated_at": NOW, "n_docs": N,
             "idf": {t: round(idf[t], 4) for t in keep_terms},
             "docs": docs}
    (BRAIN / "tfidf-model.json").write_text(
        json.dumps(model, ensure_ascii=False), encoding="utf-8")
    print(f"[write] tfidf-model.json ({len(keep_terms)} terms, {N} vectors)")


# --------------------------------------------------------------------------- #
def write_triples(atoms, concepts):
    """Subject-Predicate-Object triples for multi-hop GraphRAG reasoning."""
    id_by_path = {a["path"]: a["id"] for a in atoms}
    triples = []
    for a in atoms:
        triples.append([a["path"], "in_codex", a["codex"]])
        triples.append([a["path"], "in_section", f"{a['codex']}/{a['section']}"])
        for h in a["h2"][:15]:
            c = norm_concept(h)
            if 3 <= len(c) <= 80 and not is_boilerplate(c):
                triples.append([a["path"], "teaches", c])
        for t in a["links"]:
            if t in id_by_path:
                triples.append([a["path"], "links_to", t])
        for u in a["url_links"][:10]:
            triples.append([a["path"], "cites_url", u])
    (BRAIN / "graph" / "triples.json").write_text(
        json.dumps({"generated_at": NOW, "count": len(triples),
                    "predicates": sorted({t[1] for t in triples}),
                    "triples": triples}, ensure_ascii=False), encoding="utf-8")
    print(f"[write] graph/triples.json ({len(triples)} triples)")


# --------------------------------------------------------------------------- #
def write_bridges(atoms, concepts):
    """Cross-codex bridges: concepts taught in BOTH codices (transfer learning)."""
    codex_of = {a["path"]: a["codex"] for a in atoms}
    bridges = []
    for r in concepts.values():
        by_codex = {}
        for p in r["docs"]:
            by_codex.setdefault(codex_of.get(p, "?"), []).append(p)
        if len(by_codex) > 1:
            bridges.append({"concept": r["concept"],
                            "codices": {c: v[:5] for c, v in by_codex.items()}})
    bridges.sort(key=lambda b: -sum(len(v) for v in b["codices"].values()))
    (BRAIN / "bridges.json").write_text(
        json.dumps({"generated_at": NOW, "count": len(bridges),
                    "bridges": bridges}, indent=2, ensure_ascii=False),
        encoding="utf-8")
    print(f"[write] bridges.json ({len(bridges)} cross-codex concepts)")


# --------------------------------------------------------------------------- #
def write_context_pack(atoms, codices, sections, concepts):
    """One file to bootstrap ANY AI: the whole codex compressed to fit a context
    window — stats, every section summary, top concepts, and how to query."""
    total_words = sum(a["words"] for a in atoms)
    L = ["# 🧠 SECOND BRAIN — CONTEXT PACK (single-file bootstrap)", "",
         f"Load this one file to gain a working model of the entire {total_words:,}-word",
         f"corpus ({len(atoms)} docs, {len(codices)} codices, {len(sections)} sections).",
         "", "## How to recall the full detail (no context limit)",
         "```",
         "python .second-brain/brain.py ask \"<natural-language question>\"   # TF-IDF semantic",
         "python .second-brain/brain.py search \"<keywords>\"                 # SQLite FTS5",
         "python .second-brain/brain.py related <path> | concept <term> | outline",
         "```", ""]
    for c in sorted(codices):
        secs = sorted({s for (cc, s) in sections if cc == c})
        L.append(f"\n## {c} — {len(codices[c])} docs")
        for s in secs:
            paths = sorted(sections[(c, s)])
            freq = {}
            for p in paths:
                a = next(x for x in atoms if x["path"] == p)
                for t in a["h2"]:
                    k = norm_concept(t).lower()
                    if k and not is_boilerplate(k):
                        freq[k] = freq.get(k, 0) + 1
            top = ", ".join(t for t, _ in sorted(freq.items(), key=lambda kv: -kv[1])[:10])
            L.append(f"- **{s}** ({len(paths)}): {top}")
    top_concepts = sorted(concepts.values(), key=lambda r: -len(r["docs"]))[:80]
    L.append("\n## Top concepts (by breadth)")
    L.append(", ".join(r["concept"] for r in top_concepts))
    (BRAIN / "context-pack.md").write_text("\n".join(L), encoding="utf-8")
    print("[write] context-pack.md")


# --------------------------------------------------------------------------- #
def write_finetune_dataset(atoms):
    """Instruction/response pairs for fine-tuning or eval, in chat + alpaca formats."""
    (BRAIN / "training").mkdir(exist_ok=True)
    alpaca, chat = [], []
    for a in atoms:
        if not a["h2"]:
            continue
        topics = "; ".join(a["h2"][:12])
        out = (f"'{a['title']}' (in {a['codex']}/{a['section']}, file {a['path']}) "
               f"covers: {topics}.")
        instr = f"What does the codex document '{a['title']}' teach, and where is it?"
        alpaca.append({"instruction": instr, "input": "", "output": out})
        chat.append({"messages": [
            {"role": "system", "content": f"You are an expert with perfect "
             f"recall of the {PROJECT_NAME} knowledge base."},
            {"role": "user", "content": instr},
            {"role": "assistant", "content": out}]})
    with (BRAIN / "training" / "finetune-alpaca.jsonl").open("w", encoding="utf-8") as f:
        for r in alpaca:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with (BRAIN / "training" / "finetune-chat.jsonl").open("w", encoding="utf-8") as f:
        for r in chat:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"[write] training/finetune-*.jsonl ({len(alpaca)} pairs)")


# --------------------------------------------------------------------------- #
def write_schemas():
    (BRAIN / "schemas").mkdir(exist_ok=True)
    manifest_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "SecondBrainManifest", "type": "object",
        "required": ["generated_at", "stats", "documents"],
        "properties": {
            "generated_at": {"type": "string"},
            "stats": {"type": "object"},
            "documents": {"type": "array", "items": {
                "type": "object",
                "required": ["id", "path", "title", "codex"],
                "properties": {
                    "id": {"type": "string"}, "path": {"type": "string"},
                    "title": {"type": "string"}, "codex": {"type": "string"},
                    "links": {"type": "array", "items": {"type": "string"}}}}}},
    }
    graph_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "KnowledgeGraph", "type": "object",
        "required": ["nodes", "edges"],
        "properties": {
            "nodes": {"type": "array", "items": {"type": "object",
                      "required": ["id", "type"]}},
            "edges": {"type": "array", "items": {"type": "object",
                      "required": ["source", "target", "type"]}}},
    }
    (BRAIN / "schemas" / "manifest.schema.json").write_text(
        json.dumps(manifest_schema, indent=2), encoding="utf-8")
    (BRAIN / "schemas" / "knowledge-graph.schema.json").write_text(
        json.dumps(graph_schema, indent=2), encoding="utf-8")
    print("[write] schemas/*.schema.json")


# --------------------------------------------------------------------------- #
def write_editor_tasks():
    """VS Code tasks to run the brain, without clobbering an existing config."""
    tasks = {
        "version": "2.0.0",
        "tasks": [
            {"label": "Second Brain: Rebuild", "type": "shell",
             "command": "python .second-brain/build_second_brain.py",
             "problemMatcher": []},
            {"label": "Second Brain: Search", "type": "shell",
             "command": "python .second-brain/brain.py search \"${input:q}\"",
             "problemMatcher": []},
            {"label": "Second Brain: Ask (semantic)", "type": "shell",
             "command": "python .second-brain/brain.py ask \"${input:q}\"",
             "problemMatcher": []},
            {"label": "Second Brain: Doctor", "type": "shell",
             "command": "python .second-brain/brain.py doctor",
             "problemMatcher": []},
        ],
        "inputs": [{"id": "q", "type": "promptString",
                    "description": "Second Brain query"}],
    }
    payload = json.dumps(tasks, indent=2)
    (BRAIN / "editor").mkdir(exist_ok=True)
    (BRAIN / "editor" / "tasks.example.json").write_text(payload, encoding="utf-8")
    vscode = REPO_ROOT / ".vscode"
    if not (vscode / "tasks.json").exists():
        vscode.mkdir(exist_ok=True)
        (vscode / "tasks.json").write_text(payload, encoding="utf-8")
    print("[write] editor/tasks.example.json (+ .vscode/tasks.json if absent)")


# --------------------------------------------------------------------------- #
def write_broken_links(atoms):
    known = {a["path"]: a for a in atoms}
    broken = []
    for a in atoms:
        for t in a["out_links_raw"]:
            if resolve_link(a["path"], t, known) is None:
                broken.append((a["path"], t))
    lines = [f"# 🔗 Broken internal links ({len(broken)}) — auto-generated", ""]
    for src, tgt in broken[:500]:
        lines.append(f"- `{src}` → `{tgt}`")
    (BRAIN / "broken-links.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"[write] broken-links.md ({len(broken)} broken)")


# --------------------------------------------------------------------------- #
def write_history(atoms, code_atoms, codices, sections):
    rec = {
        "at": NOW,
        "docs": len(atoms), "code_files": len(code_atoms),
        "codices": len(codices), "sections": len(sections),
        "words": sum(a["words"] for a in atoms),
        "edges": sum(len(a["links"]) for a in atoms),
    }
    hist = BRAIN / "history.jsonl"
    with hist.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    print("[write] history.jsonl (+1 snapshot)")


# --------------------------------------------------------------------------- #
def write_cache(atoms, code_atoms):
    """Content hashes for change-detection / future incremental builds."""
    cache_dir = BRAIN / ".cache"
    cache_dir.mkdir(exist_ok=True)
    cache_file = cache_dir / "hashes.json"
    prev = {}
    if cache_file.exists():
        try:
            prev = json.loads(cache_file.read_text(encoding="utf-8")).get("files", {})
        except Exception:
            prev = {}
    cur = {}
    for a in atoms + code_atoms:
        try:
            b = (REPO_ROOT / a["path"]).read_bytes()
            cur[a["path"]] = hashlib.sha1(b).hexdigest()
        except Exception:
            continue
    added = [p for p in cur if p not in prev]
    changed = [p for p in cur if p in prev and prev[p] != cur[p]]
    removed = [p for p in prev if p not in cur]
    cache_file.write_text(json.dumps(
        {"generated_at": NOW, "files": cur,
         "delta": {"added": added, "changed": changed, "removed": removed}},
        ensure_ascii=False), encoding="utf-8")
    if prev:
        print(f"[cache] +{len(added)} added, ~{len(changed)} changed, -{len(removed)} removed")
    else:
        print(f"[cache] baseline of {len(cur)} files recorded")


# --------------------------------------------------------------------------- #
def validate_build(atoms):
    """Self-healing check: verify every artifact is present & parseable."""
    problems = []
    json_files = [
        "manifest.json", "concepts.json", "outline.json", "summaries.json",
        "inverted-index.json", "tfidf-model.json", "bridges.json",
        "code-index.json", "graph/knowledge-graph.json", "graph/triples.json",
        "graph/communities.json",
    ]
    for jf in json_files:
        p = BRAIN / jf
        if not p.exists():
            problems.append(f"missing {jf}")
            continue
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            problems.append(f"invalid JSON {jf}: {e}")
    for txt in ("README.md", "context-pack.md", "outline.md", "glossary.md",
                "brain.py", "brain.db"):
        if not (BRAIN / txt).exists():
            problems.append(f"missing {txt}")
    # brain.db sanity
    try:
        import sqlite3
        con = sqlite3.connect(str(BRAIN / "brain.db"))
        n = con.execute("SELECT count(*) FROM chunks").fetchone()[0]
        con.close()
        if n == 0:
            problems.append("brain.db has 0 chunks")
    except Exception as e:
        problems.append(f"brain.db error: {e}")

    report = {"validated_at": NOW, "healthy": not problems,
              "problems": problems, "documents": len(atoms)}
    (BRAIN / "validation-report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8")
    if problems:
        print(f"[VALIDATE] WARN: {len(problems)} problem(s): {problems[:5]}")
    else:
        print("[VALIDATE] OK - all artifacts present and valid")


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    build()

