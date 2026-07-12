---
inclusion: always
---
# 👤 USER PERSONA & WORKING PREFERENCES (permanent memory)

> Hand-written, not auto-generated. The second-brain generator never touches this file.
> These are the user's standing preferences. Honor them in every task.

## Core principles
1. **One place, no scattering.** Keep related work consolidated in a single folder.
   Do NOT create new sibling/top-level codices for something that belongs inside an
   existing section. Confusion is the enemy — a single clear location beats "clever"
   structure. (Example: Java lives entirely in
   `FULLSTACK-AI-GRANDMASTER-CODEX/04-JAVA-MASTERY/`, not a separate JAVA codex.)
2. **Maximum absolute depth — "nothing left."** When the user learns a topic, cover
   every sub-topic small-to-small to maximum: all terminology, all theory, practical
   runnable code, questions (self-test + interview), and pitfalls. "Reading these docs
   = complete mastery" is the bar.
3. **Step by step, part by part.** Build a complete tree/roadmap first, then walk it
   node by node in order. Never dump everything at once; never skip ahead.
4. **Avoid confusion above all.** Before restructuring, deleting, or moving existing
   files, confirm. Prefer non-destructive reorganization. Keep a single obvious entry
   point per section (one README + one tree/index), not three competing "top" files.

## The teaching method (4 layers) for every topic
🧠 Theory → ⌨️ Practical (runnable code) → ❓ Questions (with answers) → ⚠️ Pitfalls.

## ⛔ Second-brain sync: use the watcher, NEVER a Kiro hook
- The sync mechanism is **`.second-brain/watch_and_build.py`** (run it in a terminal).
- **Do NOT create a Kiro `fileEdited` runCommand hook** for rebuilds. The user
  removed it deliberately: that hook opens a NEW tab and logs a NEW history entry
  on every execution (no auto-close option), flooding the workspace. The watcher
  replaces it (one terminal, debounced, watches only content folders).
- Manual rebuild is also fine: `python .second-brain/build_second_brain.py`.

## Current active learning track
- **Java, zero → grandmaster**, entirely inside
  `FULLSTACK-AI-GRANDMASTER-CODEX/04-JAVA-MASTERY/`.
- Map/checklist: `04-JAVA-MASTERY/00-COMPLETE-TREE.md` (14 phases, 0–13).
- Proceed phase by phase on the user's cue ("start Phase 0", "teach 1.5 Strings", etc.).

## Communication
- The user often writes in Hinglish; mirror lightly, stay clear and direct.
