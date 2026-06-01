# 🖥️ Browsers and Rendering

> *"The browser is the most sophisticated piece of software most people use daily — and the runtime your frontend code actually lives in. Understand it, and React stops being magic."*

The server sent back a response (previous chapter). Now the **browser** must turn that stream of HTML, CSS, and JavaScript into the pixels, layout, and interactivity a human sees. This chapter is about *how* — the rendering pipeline, the DOM and CSSOM, what makes pages slow (reflow/repaint), and an introduction to the event loop that powers all JavaScript. This is the foundation React and every frontend framework build on.

---

## I. WHAT A BROWSER ACTUALLY IS

A browser is several engines working together:

| Engine | Job | Examples |
|---|---|---|
| **Networking** | Fetches resources over HTTP(S) | (built in) |
| **Rendering / layout engine** | Parses HTML/CSS, computes layout, paints pixels | Blink (Chrome/Edge), WebKit (Safari), Gecko (Firefox) |
| **JavaScript engine** | Parses and executes JS | V8 (Chrome/Node), JavaScriptCore (Safari), SpiderMonkey (Firefox) |

Crucially, **V8 (the JS engine) and Blink (the rendering engine) are separate but cooperating.** JavaScript can change the page, and rendering reflects those changes — but they share resources in ways that explain a lot of performance behavior (see §VII).

---

## II. THE CRITICAL RENDERING PATH

When HTML arrives, the browser runs a pipeline often called the **Critical Rendering Path (CRP)**. This is the single most important diagram in frontend performance:

```
  HTML bytes                 CSS bytes
      │                          │
      ▼ parse                    ▼ parse
  ┌────────┐                ┌─────────┐
  │  DOM   │                │ CSSOM   │      DOM   = structure/content tree
  └───┬────┘                └────┬────┘      CSSOM = all the computed styles
      │                          │
      └────────────┬─────────────┘
                   ▼ combine
            ┌──────────────┐
            │ RENDER TREE  │     only visible nodes + their styles
            └──────┬───────┘
                   ▼
            ┌──────────────┐
            │   LAYOUT     │     compute exact position & size of every box ("reflow")
            └──────┬───────┘
                   ▼
            ┌──────────────┐
            │   PAINT      │     fill in pixels: text, colors, borders, images
            └──────┬───────┘
                   ▼
            ┌──────────────┐
            │  COMPOSITE   │     assemble layers in the correct order → screen
            └──────────────┘
```

Let's walk each stage.

### 1. Parse HTML → DOM
The browser reads HTML top-to-bottom and builds the **DOM** (Document Object Model): a tree of objects, one per element, representing the page's structure and content.

```html
<html>
  <body>
    <h1>Hello</h1>
    <p>World</p>
  </body>
</html>
```
becomes the tree:
```
Document
└── html
    └── body
        ├── h1 → "Hello"
        └── p  → "World"
```

The DOM is **live and programmable** — JavaScript manipulates *this tree*, not the original HTML text. Change the DOM, and the page updates.

### 2. Parse CSS → CSSOM
In parallel, the browser parses all CSS (inline, `<style>`, and external `<link>` stylesheets) into the **CSSOM** (CSS Object Model) — a tree of all the computed style rules and how they cascade.

> **CSS is render-blocking.** The browser won't paint until it has the CSSOM, because painting without final styles would show a flash of unstyled or wrongly-styled content. This is why you put CSS in the `<head>` and keep it lean.

### 3. Render tree = DOM + CSSOM
The browser combines the two into the **render tree** — only the nodes that will actually be *displayed*, each paired with its computed styles. Notably, `display: none` elements and `<head>` are **excluded** (they're in the DOM but not rendered). Note: `visibility: hidden` elements *stay* in the render tree (they occupy space; they're just invisible).

### 4. Layout (a.k.a. reflow)
The browser calculates the exact **geometry** — where every box goes and how big it is — based on the viewport size and the box model. This is **layout** (Firefox calls it "reflow"). It's expensive because changing one element can shift many others.

### 5. Paint
The browser fills in the actual pixels: text, colors, borders, shadows, images. The result is split into **layers**.

### 6. Composite
Layers are assembled in the correct order (respecting stacking, transparency, transforms) and sent to the screen. Some operations (like CSS `transform` and `opacity`) can be done at *this* stage by the GPU — which is why they're cheap to animate (more in §VII).

---

## III. THE DOM IN PRACTICE

The DOM is the bridge between your HTML and your JavaScript. Every frontend interaction is, ultimately, reading or changing the DOM.

```javascript
// Reading the DOM
const heading = document.querySelector("h1");
console.log(heading.textContent);          // "Hello"

// Changing the DOM (the page updates immediately)
heading.textContent = "Hello, DOM!";
heading.style.color = "crimson";

// Creating and inserting a new node
const li = document.createElement("li");
li.textContent = "New item";
document.querySelector("ul").appendChild(li);

// Responding to events (interactivity)
document.querySelector("button").addEventListener("click", () => {
  alert("Clicked!");
});
```

> **Key insight for later:** React exists largely to *manage* DOM updates for you. Direct DOM manipulation is fine for small pages but becomes error-prone at scale — which is exactly the problem React's virtual DOM and declarative model solve. You'll appreciate React far more having done this by hand first (that's your build gate before learning React).

---

## IV. HOW JAVASCRIPT BLOCKS RENDERING

The browser parses HTML top-to-bottom. When it hits a `<script>`, by default it **stops, downloads, and executes** the script before continuing — because the script might change the DOM. This is **render-blocking** and a classic cause of slow first paint.

```html
<!-- BAD: blocks HTML parsing until the script downloads + runs -->
<head>
  <script src="big-app.js"></script>
</head>

<!-- BETTER: load in parallel, execute after HTML is parsed, in order -->
<head>
  <script src="big-app.js" defer></script>
</head>

<!-- ALSO: load in parallel, execute as soon as ready (order NOT guaranteed) -->
<head>
  <script src="analytics.js" async></script>
</head>
```

| Attribute | Download | Execute | Order preserved? | Use for |
|---|---|---|---|---|
| (none) | blocks parsing | immediately | yes | rarely — avoid in `<head>` |
| `defer` | parallel | after HTML parsed | ✅ yes | your app scripts |
| `async` | parallel | as soon as downloaded | ❌ no | independent scripts (analytics) |

> **Rule of thumb:** use `defer` for scripts that touch the DOM and depend on order; use `async` for self-contained scripts. Or place scripts at the end of `<body>`.

---

## V. THE EVENT LOOP (INTRODUCTION)

JavaScript in the browser is **single-threaded** — it runs one thing at a time on one "main thread." Yet pages handle clicks, timers, and network responses seemingly at once. The mechanism that makes this possible is the **event loop**.

### The pieces

```
   ┌─────────────────────────┐
   │      CALL STACK         │   where the currently-running function lives
   │  (one thing at a time)  │
   └───────────┬─────────────┘
               │ when empty, the event loop pulls the next task ↓
   ┌───────────▼─────────────┐        ┌──────────────────────────┐
   │   MICROTASK QUEUE       │  then  │      TASK (macro) QUEUE  │
   │  (Promises, queueMicro) │ ◀────  │ (setTimeout, events, I/O)│
   └─────────────────────────┘        └──────────────────────────┘
        higher priority                     lower priority
```

- **Call stack** — runs synchronous code, one frame at a time.
- **Web APIs** — the browser (not JS itself) handles timers, network requests, DOM events *off* the main thread.
- When those finish, their callbacks are queued: **microtasks** (Promise callbacks) and **macrotasks** (`setTimeout`, events).
- The **event loop**: whenever the call stack is empty, it drains *all* microtasks, then takes *one* macrotask, then repeats — interleaving rendering.

### The classic example

```javascript
console.log("1: sync start");

setTimeout(() => console.log("4: macrotask (setTimeout)"), 0);

Promise.resolve().then(() => console.log("3: microtask (promise)"));

console.log("2: sync end");

// Output order:
// 1: sync start
// 2: sync end
// 3: microtask (promise)      ← microtasks run before macrotasks
// 4: macrotask (setTimeout)   ← even though the timeout was 0ms
```

**Why this order?** All synchronous code runs first (1, 2). Then the stack is empty, so the loop drains microtasks (3) *before* touching the macrotask queue (4). `setTimeout(fn, 0)` does **not** mean "run now" — it means "run after the current work and all microtasks finish."

> **Why it matters:** This single-threaded model is why a long synchronous loop **freezes the entire page** — clicks, scrolling, animation, everything. Heavy work must be broken up, deferred, or moved to a Web Worker. You'll revisit the event loop in depth in `02-JAVASCRIPT-MASTERY`; here, just hold the mental model.

```javascript
// This freezes the whole tab for seconds — nothing else can run:
function blockEverything() {
  const end = Date.now() + 5000;
  while (Date.now() < end) { /* busy loop, main thread is hostage */ }
}
```

---

## VI. REFLOW AND REPAINT — THE PERFORMANCE CORE

Once a page is rendered, changing it can re-trigger parts of the pipeline. Two costs to know:

- **Reflow (layout)** — recomputing geometry (positions/sizes). **Expensive** — can cascade to many elements. Triggered by changing width/height, adding/removing elements, font changes, reading layout properties like `offsetHeight`.
- **Repaint** — redrawing pixels without changing layout (e.g. color change). **Cheaper** than reflow, but still costs.
- **Composite-only** — changes handled by the GPU at the compositing stage (CSS `transform`, `opacity`). **Cheapest** — no layout, no paint.

```
Change layout (width, top, adding nodes)  →  Reflow → Repaint → Composite   (most expensive)
Change paint  (color, background, shadow) →           Repaint → Composite   (medium)
Change transform / opacity                →                     Composite   (cheapest — prefer these!)
```

### Practical consequences

```javascript
// BAD: forces "layout thrashing" — repeated reflows in a loop.
// Reading offsetHeight forces a reflow; writing height invalidates layout again. Interleaved = disaster.
for (let i = 0; i < boxes.length; i++) {
  boxes[i].style.height = boxes[i].offsetHeight + 10 + "px"; // read-write-read-write...
}

// BETTER: batch reads, then batch writes.
const heights = boxes.map(b => b.offsetHeight);   // all reads first
boxes.forEach((b, i) => b.style.height = heights[i] + 10 + "px"); // then all writes
```

```css
/* Animate transform/opacity, NOT top/left/width — to stay on the cheap composite path */
.slide-in { transition: transform 0.3s; }      /* GPU-friendly, smooth */
/* Avoid: .slide-in { transition: left 0.3s; }  ← triggers reflow every frame */
```

> **Gotcha — layout thrashing:** Alternating DOM *writes* and layout *reads* in a loop forces the browser to recompute layout over and over (it can't batch). Read all the values you need first, then write. This single rule fixes a huge share of janky UIs.

---

## VII. THE MENTAL MODEL TO KEEP

```
1. Browser fetches HTML  → builds DOM
2. Browser fetches CSS   → builds CSSOM   (render-blocking)
3. DOM + CSSOM           → render tree
4. Render tree           → LAYOUT (geometry)
5. Layout                → PAINT (pixels)
6. Paint                 → COMPOSITE (layers → screen)
   ── JavaScript runs on a single thread, scheduled by the EVENT LOOP,
      and can mutate the DOM/CSSOM, re-triggering layout/paint/composite ──
```

Almost every frontend performance question reduces to: *"Which stage of this pipeline am I forcing the browser to redo, how often, and can I move it to a cheaper stage?"*

---

## VIII. COMMON PITFALLS / GOTCHAS

- **`<script>` in `<head>` without `defer`** blocks parsing → blank page longer than necessary. Use `defer`.
- **Layout thrashing** — interleaving DOM reads and writes in a loop forces repeated reflows. Batch reads, then writes.
- **Animating `top`/`left`/`width`/`height`** triggers reflow every frame → jank. Animate `transform` and `opacity` instead.
- **Believing `setTimeout(fn, 0)` runs immediately.** It runs *after* current sync code and all microtasks.
- **Long synchronous loops** freeze the whole tab — the single thread can't do anything else. Break up or offload heavy work.
- **Confusing the DOM with HTML.** HTML is the initial text; the DOM is the live, in-memory tree JS manipulates. They can diverge (JS adds nodes the HTML never had).
- **`display:none` vs `visibility:hidden`.** The former leaves the render tree entirely (no space); the latter stays (invisible but occupies space).

---

## ✅ KEY TAKEAWAYS

- A browser combines a **networking engine, a rendering engine, and a JavaScript engine** that cooperate.
- The **Critical Rendering Path**: HTML→**DOM**, CSS→**CSSOM**, combined into the **render tree**, then **layout → paint → composite**.
- The **DOM** is the live, programmable tree your JavaScript reads and mutates; frameworks like React exist to manage these updates for you.
- CSS is **render-blocking** and `<script>` is **parser-blocking** by default — use `defer`/`async` and keep CSS lean.
- JavaScript is **single-threaded**; the **event loop** drains all microtasks (Promises) before each macrotask (`setTimeout`, events), interleaving rendering. A long sync task freezes the page.
- Performance work = minimizing **reflow** (layout) and **repaint**, and preferring **composite-only** changes (`transform`, `opacity`). Avoid **layout thrashing** by batching reads then writes.

---

**→ Next:** [`04-HTML-Essentials.md`](./04-HTML-Essentials.md) — the structure the browser parses
**← Prev:** [`02-HTTP-And-HTTPS.md`](./02-HTTP-And-HTTPS.md)
**🗺️ Index:** [`00-Index.md`](./00-Index.md)
