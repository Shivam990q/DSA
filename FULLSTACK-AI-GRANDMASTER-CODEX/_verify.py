import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r"c:\Users\Rose\Videos\FUTURE\DSA\FULLSTACK-AI-GRANDMASTER-CODEX"

for section in sorted(os.listdir(ROOT)):
    sp = os.path.join(ROOT, section)
    if not os.path.isdir(sp):
        continue
    files = sorted(f for f in os.listdir(sp) if f.endswith('.md'))
    total = 0
    print(f"\n=== {section} ({len(files)} md files) ===")
    for f in files:
        fp = os.path.join(sp, f)
        with open(fp, encoding='utf-8') as fh:
            lc = sum(1 for _ in fh)
        total += lc
        print(f"  {lc:5d}  {f}")
    print(f"  ---- total lines: {total}")
