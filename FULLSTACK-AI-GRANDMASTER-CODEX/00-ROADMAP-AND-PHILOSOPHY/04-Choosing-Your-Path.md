# 🧭 Choosing Your Path

> *"You can learn everything eventually. You cannot learn everything at once. Pick a first destination, commit, and the rest compounds."*

This chapter helps you choose where to aim first: **Frontend**, **Backend**, **Full-Stack**, or **AI**. It covers what each role actually does day-to-day, the tradeoffs, what the work *feels* like, and rough compensation context. There is no "best" path — only the best fit for *your* interests and *your* market.

> **On salary numbers:** figures below are broad, US-leaning ranges and vary enormously by country, city, company size, and experience. Treat them as *relative* signals (how roles compare to each other), not promises. Verify current local numbers on sites like [levels.fyi](https://www.levels.fyi/), [Glassdoor](https://www.glassdoor.com/), or the [Stack Overflow Developer Survey](https://survey.stackoverflow.co/). *Content rephrased and generalized for compliance.*

---

## I. THE FOUR PATHS AT A GLANCE

| Path | You build... | Core skills | Vibe | Codex folders |
|---|---|---|---|---|
| **Frontend** | What users see & touch | HTML, CSS, JS, React, Next.js | Visual, immediate feedback, UX-focused | 01, 02, 03, 05, 06 |
| **Backend** | The logic & data behind the scenes | APIs, databases, auth, servers | Systems, correctness, scale | 01, 02/04, 07, 08, 09 |
| **Full-Stack** | The whole thing, end to end | All of the above | Versatile, big-picture, "glue" | All of 01–11 |
| **AI/ML** | Intelligent features & models | Math, ML, LLMs, data | Experimental, research-flavored | 12 (+ 01,07,11 to ship) |

---

## II. FRONTEND ENGINEER

### What you do day-to-day
Turn designs into living interfaces. Build components, handle user interactions, manage UI state, make things fast and accessible, ensure it works across browsers and screen sizes. You live in the browser and obsess over the user experience.

### A day might include
- Implementing a new screen from a Figma design.
- Fixing a layout that breaks on mobile.
- Making a list render smoothly with 10,000 items.
- Wiring a form to a backend API and handling loading/error states.
- Improving accessibility (keyboard navigation, screen-reader labels).

### You'll enjoy it if...
- You like **immediate visual feedback** — change code, see it instantly.
- You care about **design, polish, and how things feel** to use.
- You enjoy the puzzle of making complex interactions feel simple.

### You might dislike it if...
- You're frustrated by **browser quirks** and CSS edge cases.
- You prefer problems with one provably-correct answer over subjective "does this feel right?"

### Tradeoffs
| Pros | Cons |
|---|---|
| Fast, satisfying feedback loop | CSS/browser inconsistencies can be maddening |
| Lower math barrier to entry | Fast-churning tools (new framework every year) |
| Highly visible impact | Sometimes seen (wrongly) as "less serious" engineering |

### Comp context
Generally comparable to backend at the same level; can dip slightly lower at the *junior* end and is very strong at senior/staff when paired with deep performance, accessibility, and architecture skills.

---

## III. BACKEND ENGINEER

### What you do day-to-day
Build the engine behind the app: design APIs, model and query databases, implement business rules, handle authentication, integrate third-party services, and make it all correct, secure, and able to handle load. Users never see your work directly — they feel it as speed and reliability.

### A day might include
- Designing a REST (or GraphQL) endpoint and its data model.
- Writing and optimizing a slow database query.
- Adding authentication/authorization to protect resources.
- Debugging why a service falls over under heavy traffic.
- Setting up a background job or message queue.

### You'll enjoy it if...
- You like **systems thinking**, data modeling, and provable correctness.
- You enjoy **performance and scale** problems.
- You'd rather get the architecture right than pick a button color.

### You might dislike it if...
- You miss **visual feedback** — backend wins are invisible.
- You dislike on-call / production-incident pressure (the backend is where outages hurt).

### Tradeoffs
| Pros | Cons |
|---|---|
| Deep, durable fundamentals (SQL, HTTP age slowly) | Less immediately visible work |
| High demand, strong pay | Production incidents and on-call |
| Clear notions of "correct" | Complexity hides in data and concurrency |

### Comp context
Strong and stable. Specializations (distributed systems, databases, infrastructure) are among the best-paid non-management tracks.

---

## IV. FULL-STACK ENGINEER

### What you do day-to-day
Everything above — you move fluidly between the browser, the server, and the database. You can take a feature from idea to deployed reality by yourself: build the UI, the API it calls, the table it stores into, and ship it.

### A day might include
- Building a feature end-to-end: React component → Express endpoint → MongoDB collection.
- Debugging an issue that could be in *any* layer and tracing it down the stack.
- Setting up deployment so the whole thing runs in the cloud.
- Switching context several times a day between very different kinds of problems.

### You'll enjoy it if...
- You like **owning the whole picture** and shipping complete features.
- You're a generalist who gets bored doing only one layer.
- You value **versatility** (great for startups, freelancing, founding).

### You might dislike it if...
- You prefer going **very deep** in one specialty over being broad.
- Constant context-switching drains you.

### Tradeoffs
| Pros | Cons |
|---|---|
| Most versatile; can build anything solo | Hard to be deepest-expert in every layer |
| Ideal for startups & founders | More to keep current with |
| Strong market demand | Risk of being "jack of all trades" without deliberate depth |

### Comp context
Very employable, especially at startups and mid-size companies that value one person covering multiple layers. At large companies, deep specialists sometimes out-earn generalists at the very top — so most full-stack engineers still cultivate one area of genuine depth.

> **Reality check:** "full-stack" doesn't mean *equally expert* at everything. It means *competent across the stack with depth in one or two areas.* The codex's Path E aims you here.

---

## V. AI / ML ENGINEER

This path has two distinct flavors — be clear which you mean.

### Flavor A: AI *Application* Engineer (the fast, practical entry)
You **integrate** existing models (OpenAI, open-source LLMs) into products: chatbots, RAG systems over company data, semantic search, AI features in normal apps. This is mostly *strong software engineering* + understanding model APIs, prompting, embeddings, and retrieval. **Reachable from this codex** after the full-stack stages plus folder 12.

### Flavor B: ML *Research/Modeling* Engineer (the deep, mathematical entry)
You **build and train** models: design architectures, run experiments, work with the math (linear algebra, probability, calculus, optimization). Often expects a stronger math background and frequently a graduate degree for research roles.

### A day might include
- *(App)* Building a retrieval pipeline, tuning prompts, evaluating output quality, wiring an LLM into a web app.
- *(Modeling)* Cleaning datasets, training/fine-tuning models, reading papers, running and analyzing experiments.

### You'll enjoy it if...
- You're comfortable with **uncertainty** — results are probabilistic, not pass/fail.
- *(Modeling)* You **love math and research**, reading papers, experimentation.
- *(App)* You like riding the **newest wave** and shipping novel features.

### You might dislike it if...
- You want deterministic, "it works or it doesn't" outcomes.
- *(Modeling)* You dislike heavy math or open-ended research.

### Tradeoffs
| Pros | Cons |
|---|---|
| Highest-growth, high-comp field right now | Fastest-changing; today's technique is obsolete quickly |
| Intellectually thrilling | Modeling roles have a steep math/degree barrier |
| Huge demand for *applied* AI builders | Probabilistic results are hard to test and debug |

### Comp context
Among the highest in the industry, especially for experienced ML/research engineers at top labs. *Applied* AI engineering (Flavor A) is increasingly just well-paid software engineering with an AI specialty — a realistic, high-leverage target for full-stack graduates of this codex.

---

## VI. HOW TO ACTUALLY DECIDE

Don't overthink the *forever* choice — pick a strong *first* destination. You can pivot; the fundamentals transfer.

### A quick self-quiz
- **"I want to *see* my work and care how it looks/feels."** → Frontend.
- **"I want to solve systems/data problems; I don't need it to be pretty."** → Backend.
- **"I want to build whole products and maybe start companies."** → Full-Stack.
- **"I'm pulled toward math, data, and the cutting edge."** → AI (modeling), or Full-Stack → AI *application* for a faster route.
- **"I have no idea."** → **Full-Stack.** It exposes you to every layer; you'll discover your preference by doing, and nothing is wasted.

### The strategic recommendation
For most beginners, **start full-stack (Path A)** even if you suspect you'll specialize. Reasons:
1. You can't know what you like until you've touched each layer.
2. Full-stack skills make you employable *while* you specialize.
3. Every specialty is stronger when you understand its neighbors — frontend engineers who get backends, and AI engineers who can ship apps, are far more valuable.

Then, once you've built a couple of full apps, **deepen** in whichever layer pulled you hardest.

---

## VII. COMMON PITFALLS / GOTCHAS

- **Choosing by salary alone.** You'll do this work ~40 hours a week for years. Interest sustains you through the hard parts; a number won't.
- **Believing the choice is permanent.** It isn't. Engineers switch specialties regularly; the fundamentals (this codex's foundations) carry over.
- **Picking AI to skip the "boring" fundamentals.** Even AI *application* roles need solid software engineering to ship and debug. There's no shortcut around the basics.
- **Going too narrow too early.** Specializing before you've seen the whole stack means choosing blind. Taste the layers first.
- **Comparing your start to someone's middle.** A senior in any path was once where you are. Path matters less than consistency.

---

## ✅ KEY TAKEAWAYS

- Four paths: **Frontend** (what users see), **Backend** (logic & data), **Full-Stack** (the whole thing), **AI/ML** (intelligent features/models).
- Each has a distinct *daily feel*: visual & immediate (frontend), systems & correctness (backend), versatile & big-picture (full-stack), experimental & probabilistic (AI).
- **Comp is broadly comparable across web paths**; top AI/ML and deep specialists lead at the high end — but interest and consistency matter more than the starting number.
- AI splits into **application** (reachable after full-stack + folder 12) and **modeling/research** (heavier math, often a degree).
- **When unsure, start full-stack**, then deepen into whatever pulled you hardest. The choice isn't permanent, and the fundamentals transfer.

---

**→ Next:** [`../01-WEB-FOUNDATIONS/00-Index.md`](../01-WEB-FOUNDATIONS/00-Index.md) — begin the real work: how the web actually works
**← Prev:** [`03-How-The-Web-Works-Overview.md`](./03-How-The-Web-Works-Overview.md)
**🗺️ Index:** [`00-Index.md`](./00-Index.md)
