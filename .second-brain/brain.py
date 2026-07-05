#!/usr/bin/env python3
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
