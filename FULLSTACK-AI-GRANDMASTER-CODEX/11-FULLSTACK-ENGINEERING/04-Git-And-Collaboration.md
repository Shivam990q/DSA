# 🌿 04 — Git & Collaboration

> *"Git is a time machine, a safety net, and a conversation between every engineer who ever touched the code. Master it and you stop fearing change — you start orchestrating it."*

**Prev:** [`03-Testing-Strategies.md`](./03-Testing-Strategies.md) · **Next:** [`05-Docker-And-Containers.md`](./05-Docker-And-Containers.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. THE GIT MENTAL MODEL — SNAPSHOTS, NOT DIFFS

Most tools store changes as *deltas* (file A changed these lines). Git is different: **every commit is a full snapshot** of your project, with unchanged files stored as pointers to identical previous content. Internally it's a content-addressed key-value store — Git hashes content with SHA-1/SHA-256 and that hash *is* the address.

```
A commit = snapshot of the whole tree + metadata
   ┌─────────────────────────────┐
   │ commit a3f9c1                │
   │  tree   → snapshot of files  │
   │  parent → previous commit    │   ← links form a chain
   │  author, message, timestamp  │
   └─────────────────────────────┘
```

Commits form a **DAG** (directed acyclic graph): each commit points to its parent(s), branches are just movable pointers into this graph, and a merge commit has two parents.

```
A ── B ── C ── D      (main)
            \
             E ── F   (feature)   ← F's parent is E, E's parent is C
```

> **Gotcha — a commit is identified by its SHA, which depends on its *entire history*.** Change anything about a commit (message, content, parent) and you get a *new* SHA — a different commit. This is why rewriting history (rebase, amend) creates new commits rather than editing old ones, and why force-pushing shared history is dangerous (§VI).

---

## II. THE THREE TREES & CORE WORKFLOW

Git moves changes through three areas. Understanding them demystifies almost every command:

```
Working Directory  ──git add──▶  Staging Area (Index)  ──git commit──▶  Repository (.git)
  (your edits)                     (the next snapshot)                   (permanent history)
```

- **Working directory** — the files you actually edit.
- **Staging area (index)** — a draft of your next commit; you choose precisely *what* goes in.
- **Repository** — the committed, permanent history.

```bash
git init                      # create a repo (.git folder)
git status                    # what's changed / staged / untracked — run this constantly
git add file.js               # stage one file
git add -p                    # stage HUNKS interactively — craft focused commits
git commit -m "Add login validation"
git log --oneline --graph --all   # visual history of the DAG
git diff                      # working dir vs staged (unstaged changes)
git diff --staged             # staged vs last commit (what you're about to commit)
git show a3f9c1               # inspect a specific commit
```

> **Gotcha — staging is a feature, not a chore.** `git add -p` lets you split unrelated changes in one file into separate, coherent commits. A clean history of focused commits is worth far more at debugging time than a pile of "wip" blobs.

---

## III. BRANCHES, HEAD, AND THE TWO MERGES

A **branch** is just a lightweight, movable pointer to a commit. `HEAD` is a pointer to *where you are now* (usually the tip of the current branch). Creating a branch is instant — it writes one 40-char file.

```bash
git branch feature-x          # create branch (doesn't switch)
git switch feature-x          # switch to it (modern; was `git checkout`)
git switch -c feature-x       # create AND switch in one step
git branch -d feature-x       # delete a merged branch
```

### Fast-forward vs 3-way merge

```bash
git merge feature             # merge feature into the current branch
```

```
FAST-FORWARD (main hasn't moved since branching):
  main just slides forward — no merge commit needed
  A ── B ── C          →     A ── B ── C ── D ── E   (main = feature tip)
            \
             D ── E (feature)

3-WAY MERGE (both branches advanced):
  Git finds the common ancestor (C) and creates a MERGE COMMIT (M) with two parents
  A ── B ── C ── D ── G (main)            A ─ B ─ C ─ D ─ G ─── M (main)
              \                    →                  \      /
               E ── F (feature)                        E ── F
```

> **Gotcha — `--no-ff` preserves feature-branch grouping.** A fast-forward erases the fact that a set of commits belonged to one feature. Teams often `git merge --no-ff` to always create a merge commit, keeping the branch's commits visibly grouped in history.

---

## IV. MERGE vs REBASE — AND THE GOLDEN RULE

Both integrate changes from one branch into another, but they produce different histories.

**Merge** preserves history exactly and adds a merge commit. **Rebase** *replays* your commits on top of another branch, creating new commits with new SHAs — a clean, linear history.

```bash
# You're on feature; main moved ahead. Two ways to catch up:

git merge main          # MERGE: adds a merge commit; history shows the actual branching
git rebase main         # REBASE: moves your commits to sit on top of main's tip; linear
```

```
REBASE result — feature's commits (E', F') are NEW commits replayed onto main's tip:
  A ── B ── C ── D ── G (main)
                       \
                        E' ── F' (feature)   ← linear, as if you branched from G
```

| | **Merge** | **Rebase** |
|---|---|---|
| History | True, with merge commits | Linear, rewritten |
| SHAs | Preserved | New (commits recreated) |
| Conflicts | Resolved once | Possibly once per replayed commit |
| Best for | Integrating shared branches | Cleaning up *your own* local commits |

> **⚠️ THE GOLDEN RULE OF REBASE: never rebase commits that others have pulled.** Rebasing rewrites history (new SHAs). If teammates based work on the old commits, you've forked reality — their pulls conflict catastrophically. **Rebase only local, unpushed commits.** Merge for anything shared.

```bash
git rebase -i HEAD~3          # interactive: squash/reword/reorder your last 3 LOCAL commits
# pick / squash / fixup / reword / drop — clean up before opening a PR
```

---

## V. BRANCHING STRATEGIES

How a team organizes branches shapes its whole delivery rhythm.

| Strategy | Branches | Best for | Tradeoff |
|----------|----------|----------|----------|
| **Git Flow** | `main`, `develop`, `feature/*`, `release/*`, `hotfix/*` | Versioned releases, scheduled shipping | Heavy; lots of branches & ceremony |
| **GitHub Flow** | `main` + short-lived `feature/*` | Continuous deployment, web apps | Needs strong CI & feature flags |
| **Trunk-Based** | `main` (trunk) + tiny short-lived branches | High-velocity teams, CD | Demands feature flags & fast review |

```bash
# GitHub Flow — the common modern default
git switch -c feature/add-search    # branch off main
# ...commit work...
git push -u origin feature/add-search
# open a Pull Request → review → CI passes → merge to main → deploy

# Trunk-based — merge tiny increments to main constantly; hide unfinished work behind flags
if (featureFlags.newSearch) renderNewSearch(); else renderOldSearch();
```

> **Gotcha — Git Flow is often overkill.** Its `develop`/`release` machinery suits packaged software with versioned releases. For a continuously deployed web app, it adds friction with little payoff — most teams are happier with GitHub Flow or trunk-based plus feature flags.

---

## VI. THE UNDO TOOLKIT

Git almost never truly loses work. Know which tool fits which situation:

```bash
# Undo working-directory changes (discard edits to a file)
git restore file.js                      # modern; was `git checkout -- file.js`

# Unstage (keep the edits, remove from index)
git restore --staged file.js

# Amend the LAST commit (message or forgotten file) — LOCAL only!
git commit --amend -m "Better message"

# Move the branch pointer back (rewrites local history)
git reset --soft HEAD~1     # undo commit, KEEP changes staged
git reset --mixed HEAD~1    # undo commit, keep changes unstaged (default)
git reset --hard HEAD~1     # ⚠️ undo commit AND DISCARD changes — destructive

# Undo a PUBLIC commit safely — make a NEW commit that inverts it
git revert a3f9c1           # the team-safe undo (doesn't rewrite history)

# Stash work-in-progress to switch context
git stash                   # shelve changes
git stash pop               # bring them back

# Grab a single commit from another branch
git cherry-pick a3f9c1

# The lifesaver — reflog records where HEAD has been, even after a bad reset
git reflog                  # find the lost SHA...
git reset --hard a3f9c1     # ...and recover it
```

| Need | Command | Safe on shared history? |
|------|---------|--------------------------|
| Discard file edits | `git restore` | n/a (local) |
| Unstage | `git restore --staged` | n/a (local) |
| Fix last local commit | `git commit --amend` | ❌ no |
| Undo local commit | `git reset` | ❌ no |
| Undo a pushed commit | `git revert` | ✅ yes |
| Recover "lost" commits | `git reflog` + `reset` | n/a |

> **⚠️ Gotcha — `reset --hard` and force-push destroy work.** `reset --hard` discards uncommitted changes permanently (the reflog only saves *committed* states). On shared branches, prefer `git revert`. If you must force-push, use `--force-with-lease` (it refuses if someone else pushed since you fetched) rather than `--force`.

---

## VII. CONFLICTS — RESOLVING AND AVOIDING

A conflict happens when two branches change the *same lines* differently. Git can't decide, so it marks the spot and asks you:

```
<<<<<<< HEAD
const timeout = 3000;          ← your version (current branch)
=======
const timeout = 5000;          ← incoming version (branch being merged)
>>>>>>> feature
```

```bash
git merge feature
# CONFLICT (content): Merge conflict in config.js
# ...edit the file: pick the right code, DELETE the <<<< ==== >>>> markers...
git add config.js              # mark resolved
git commit                     # (or `git rebase --continue` during a rebase)
git merge --abort              # bail out and return to pre-merge state
```

**Avoiding conflicts** beats resolving them:

- Keep branches **short-lived** — the longer a branch lives, the more it diverges.
- Pull/rebase from `main` frequently to integrate small.
- Make focused changes; avoid sprawling edits across the codebase.
- Agree on formatting (Prettier/EditorConfig) so whitespace doesn't cause phantom conflicts.

> **Gotcha — `git rerere` remembers conflict resolutions.** Enable `git config --global rerere.enabled true` and Git auto-replays how you resolved a recurring conflict (common on long-lived branches you rebase repeatedly).

---

## VIII. CONVENTIONAL COMMITS & SEMANTIC RELEASE

A consistent commit format makes history readable *and* machine-parseable for automated versioning. [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]
[optional footer]
```

```bash
git commit -m "feat(auth): add TOTP two-factor login"
git commit -m "fix(api): reject negative pagination offsets"
git commit -m "docs: clarify CORS setup in README"
git commit -m "refactor(db): extract query builder"
git commit -m "feat!: drop Node 16 support"     # ! = BREAKING CHANGE
```

| Type | Meaning | SemVer bump |
|------|---------|-------------|
| `feat` | New feature | **minor** (1.**2**.0) |
| `fix` | Bug fix | **patch** (1.2.**3**) |
| `feat!` / `BREAKING CHANGE` | Incompatible change | **major** (**2**.0.0) |
| `docs`, `style`, `refactor`, `test`, `chore` | No user-facing behavior change | none |

**Semantic release** tooling reads these messages to auto-bump the version, generate a changelog, and publish — no manual version decisions.

> **Gotcha — `feat!` / `BREAKING CHANGE` is what triggers a major bump.** Forgetting the `!` (or the footer) ships a breaking change as a minor release and breaks downstream consumers. Be deliberate about marking breaks.

---

## IX. .gitignore, .gitattributes, AND LFS

```bash
# .gitignore — files Git should never track
node_modules/          # dependencies — reinstall from lockfile
.env                   # secrets (see file 02!)
dist/  build/          # build artifacts
*.log
.DS_Store
coverage/
```

```bash
# .gitattributes — normalize line endings & mark binary/large files
* text=auto                    # normalize CRLF/LF across OSes
*.png binary                   # don't try to diff/merge binaries
*.psd filter=lfs diff=lfs merge=lfs -text   # route big files to Git LFS
```

**Git LFS (Large File Storage)** keeps large binaries (videos, datasets, design files) out of the main repo — Git stores a tiny pointer, the bytes live on an LFS server. Without it, every clone drags the full history of every huge file.

> **⚠️ Gotcha — `.gitignore` doesn't untrack already-committed files.** If you committed `node_modules` or a secret *before* adding it to `.gitignore`, it stays tracked. Run `git rm -r --cached node_modules` to stop tracking it (and for secrets, **rotate them** — file 02 — because they're in history forever).

---

## X. TAGS, RELEASES & SEMANTIC VERSIONING

**Tags** mark specific commits as releases. **Semantic Versioning** (`MAJOR.MINOR.PATCH`) communicates the nature of changes:

```
2.4.1
│ │ └─ PATCH — backward-compatible bug fixes
│ └─── MINOR — backward-compatible new features
└───── MAJOR — breaking changes
```

```bash
git tag -a v2.4.1 -m "Release 2.4.1"     # annotated tag (recommended — stores author/date/msg)
git push origin v2.4.1                     # tags aren't pushed by default
git push origin --tags                     # push all tags
git tag                                     # list tags
git checkout v2.4.0                         # inspect code at a past release
```

| Bump | When | Example |
|------|------|---------|
| MAJOR | Breaking API change | `1.9.0 → 2.0.0` |
| MINOR | New backward-compatible feature | `2.0.0 → 2.1.0` |
| PATCH | Backward-compatible bug fix | `2.1.0 → 2.1.1` |

> **Gotcha — use annotated tags (`-a`) for releases, not lightweight ones.** A lightweight tag is just a pointer with no metadata. Annotated tags store the tagger, date, and message and can be GPG-signed — what you want for an auditable release.

---

## XI. TEAMWORK — REMOTES, FORKS, PRs, HOOKS, SIGNING

```bash
# Remotes — connections to shared repos
git remote -v                       # list remotes
git remote add upstream <url>       # track the original repo (fork workflow)
git fetch origin                    # download remote changes (doesn't merge)
git pull                            # fetch + merge (or --rebase to keep linear)
git push -u origin feature/x        # push + set upstream tracking
```

**Fork workflow** (open source): fork the repo, clone *your* fork, add the original as `upstream`, branch, push to your fork, open a PR back to upstream. Keep your fork synced with `git fetch upstream && git merge upstream/main`.

**Git hooks** automate checks at lifecycle points (e.g., run lint/tests before commit):

```bash
# .husky/pre-commit — block commits that fail lint/format (via husky + lint-staged)
npx lint-staged
```

**Signed commits** prove authorship cryptographically (defends against commit spoofing):

```bash
git config --global commit.gpgsign true
git config --global user.signingkey <KEY_ID>
git commit -m "feat: signed and verified"     # shows "Verified" on GitHub
```

### Pull requests & the code review craft

A **Pull Request** is a proposal to merge a branch, plus a place to review, discuss, and run CI. Great PRs and reviews are a craft:

**As the author:**
- Keep PRs **small and focused** — a 200-line PR gets a real review; a 2,000-line PR gets a rubber stamp.
- Write a clear description: *what changed, why, how to test, what's risky.*
- Self-review the diff before requesting review. Ensure CI is green.

**As the reviewer:**
- Review for **correctness, security, readability, and tests** — not personal style preferences.
- Be kind and specific; comment on the code, not the coder. Ask questions over commands.
- Distinguish blocking issues from nits (prefix nits with "nit:").
- Approve when it's *better than before*, not when it's perfect.

> **Gotcha — large PRs get worse reviews, not more thorough ones.** Reviewer attention drops sharply with size. If a change is unavoidably big, stack it into a series of small, reviewable PRs. Small PRs ship faster *and* catch more bugs.

---

## XII. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Rebasing shared/pushed commits | Teammates' history breaks | Golden rule: rebase only local commits |
| `git reset --hard` carelessly | Uncommitted work gone | Commit/stash first; `revert` on shared branches |
| `git push --force` | Overwrites others' work | `--force-with-lease`, or never on shared |
| Committing secrets / `node_modules` | Leak / bloated repo | `.gitignore` *first*; `rm --cached`; rotate secrets |
| `.gitignore` doesn't untrack | Already-committed files persist | `git rm -r --cached <path>` |
| Giant, unfocused commits/PRs | Unreviewable, hard to revert | `git add -p`; small focused changes |
| Long-lived feature branches | Painful conflicts | Short branches; integrate often |
| Lightweight tags for releases | No metadata/signature | Annotated tags `-a` |
| Forgetting `feat!`/BREAKING | Breaking change as minor release | Mark breaks explicitly |
| Pulling with merge always | Messy non-linear history | `git pull --rebase` where appropriate |
| Thinking lost commits are gone | Panic after bad reset | `git reflog` recovers committed states |

---

## 🧠 KEY TAKEAWAYS

- Git stores **snapshots** in a **DAG**; commits are identified by content-based SHAs, so rewriting history makes *new* commits.
- Changes flow through **three trees**: working dir → staging (index) → repository. Use `git add -p` to craft focused commits.
- **Branches are cheap pointers**; merges are **fast-forward** (linear) or **3-way** (merge commit). `--no-ff` keeps features grouped.
- **Merge** preserves true history; **rebase** rewrites it linearly — and the **golden rule** is *never rebase commits others have pulled*.
- Pick a **branching strategy** to fit your cadence: GitHub Flow / trunk-based for continuous deployment, Git Flow only for versioned releases.
- The **undo toolkit** rarely loses work: `restore`, `reset`, `revert` (safe on shared), `stash`, `cherry-pick`, and `reflog` as the lifesaver. Avoid `reset --hard`/`--force` on shared history.
- Resolve conflicts by editing the marked region; **avoid** them with short branches, frequent integration, and shared formatting.
- **Conventional commits** drive **SemVer** and automated releases; mark breaking changes with `!`.
- `.gitignore` keeps junk/secrets out (but won't untrack what's already committed); use **annotated, signed tags** and **Git LFS** for big files.
- Collaboration is a craft: small focused **PRs**, kind and specific **reviews**, CI gates, hooks, and signed commits.

---

**Prev:** [`03-Testing-Strategies.md`](./03-Testing-Strategies.md) · **Next:** [`05-Docker-And-Containers.md`](./05-Docker-And-Containers.md) · **Index:** [`00-Index.md`](./00-Index.md)
