#!/usr/bin/env python3
"""
watch_and_build.py — zero-dependency background watcher for the second brain.

Why this exists
---------------
The Kiro `fileEdited` runCommand hook opens a NEW tab and logs a NEW history
entry on EVERY execution. There is no hook option to auto-close the tab or
auto-delete the history entry, so frequent saves flood the tab bar / history.

This watcher replaces that hook. It runs in ONE terminal, watches only the
codex folders, debounces bursts of saves, and rebuilds the second brain in
place — no extra tabs, no history spam.

Usage
-----
    python .second-brain/watch_and_build.py

Leave it running in a terminal while you edit. Ctrl+C to stop.
Optional: --interval <sec> poll interval (default 1.5), --debounce <sec>
quiet period before a rebuild fires (default 2.0), --once to build and exit.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent          # .../<project>/.second-brain
REPO_ROOT = SCRIPT_DIR.parent                          # .../<project>
BUILDER = SCRIPT_DIR / "build_second_brain.py"

# Only these folders should trigger a rebuild. Generated output lives elsewhere
# (.second-brain/, .kiro/, .obsidian/) so it can never retrigger the watcher.
WATCH_DIRS = [
    "DSA-Grandmaster-Codex",
    "FULLSTACK-AI-GRANDMASTER-CODEX",
    "PROGRAMMING-LANGUAGES-GRANDMASTER-CODEX",
]
WATCH_EXT = ".md"


def snapshot() -> dict[str, float]:
    """Map every watched .md file -> its mtime."""
    state: dict[str, float] = {}
    for d in WATCH_DIRS:
        base = REPO_ROOT / d
        if not base.is_dir():
            continue
        for root, _dirs, files in os.walk(base):
            for fn in files:
                if fn.lower().endswith(WATCH_EXT):
                    p = Path(root) / fn
                    try:
                        state[str(p)] = p.stat().st_mtime
                    except OSError:
                        pass
    return state


def run_build() -> None:
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] change detected -> rebuilding second brain ...", flush=True)
    try:
        proc = subprocess.run(
            [sys.executable, str(BUILDER)],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=300,
        )
        if proc.returncode == 0:
            # keep the terminal quiet: just the last summary line
            tail = [ln for ln in proc.stdout.splitlines() if ln.strip()]
            print(f"[{time.strftime('%H:%M:%S')}] done ({len(tail)} write steps).",
                  flush=True)
        else:
            print(f"[build error] exit {proc.returncode}\n{proc.stderr}", flush=True)
    except subprocess.TimeoutExpired:
        print("[build error] timed out after 300s", flush=True)
    except Exception as exc:  # pragma: no cover
        print(f"[build error] {exc}", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="Background watcher for the second brain.")
    ap.add_argument("--interval", type=float, default=1.5, help="poll seconds")
    ap.add_argument("--debounce", type=float, default=2.0, help="quiet seconds before build")
    ap.add_argument("--once", action="store_true", help="build once and exit")
    args = ap.parse_args()

    if not BUILDER.exists():
        sys.exit(f"[fatal] builder not found: {BUILDER}")

    if args.once:
        run_build()
        return

    print("Watching codex folders for .md changes. Ctrl+C to stop.")
    print("  " + "  ".join(WATCH_DIRS))
    prev = snapshot()
    pending_since: float | None = None

    try:
        while True:
            time.sleep(args.interval)
            cur = snapshot()
            if cur != prev:
                prev = cur
                pending_since = time.monotonic()  # start/refresh debounce window
            elif pending_since is not None:
                if time.monotonic() - pending_since >= args.debounce:
                    pending_since = None
                    run_build()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
