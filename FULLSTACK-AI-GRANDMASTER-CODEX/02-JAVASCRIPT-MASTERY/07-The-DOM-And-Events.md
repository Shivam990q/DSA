# 🌳 The DOM & Events

> *"The DOM is the bridge between your JavaScript and what the user actually sees."*

The **Document Object Model** is a live, tree-shaped representation of the HTML page that JavaScript can read and rewrite. This file covers selecting elements, changing them, responding to user actions with events, and the two patterns that make event handling efficient and scalable: **bubbling** and **delegation**.

> 🖥️ **Run these in a browser** (DevTools console or a `.js` file loaded by an HTML page). DOM APIs do not exist in plain Node.

---

## I. WHAT IS THE DOM?

When a browser loads HTML, it parses it into a tree of **nodes** — one object per element, attribute, and piece of text. That tree is the DOM. JavaScript manipulates the DOM; the browser re-renders to match.

```html
<!-- This HTML... -->
<body>
  <div id="app">
    <h1 class="title">Hello</h1>
    <p>World</p>
  </div>
</body>
```
```
...becomes this tree:
document
 └─ html
     └─ body
         └─ div#app
             ├─ h1.title  → "Hello"
             └─ p         → "World"
```
> The DOM is **live**: change a node in JS and the page updates. It is *not* the HTML source file — it's the in-memory model the browser builds from it (and keeps in sync).

---

## II. SELECTING ELEMENTS

```js
// Modern, preferred — CSS selector syntax
document.querySelector(".title");        // first match (or null)
document.querySelector("#app");          // by id
document.querySelector("div > p");       // any CSS selector
document.querySelectorAll("li");         // ALL matches → static NodeList

// Older, still common
document.getElementById("app");          // by id (fastest, returns element)
document.getElementsByClassName("title");// live HTMLCollection
document.getElementsByTagName("p");      // live HTMLCollection

// Scoped search (search within an element, not the whole document)
const app = document.querySelector("#app");
app.querySelector("p");                  // searches only inside #app
```

### Iterating selections
```js
// querySelectorAll returns a NodeList — has forEach but not map/filter
document.querySelectorAll("li").forEach(li => console.log(li.textContent));

// To use array methods, spread or Array.from first
const items = [...document.querySelectorAll("li")];
const texts = items.map(li => li.textContent);
```

> ⚠️ `querySelectorAll` returns a **static** snapshot. `getElementsBy*` return **live** collections that auto-update as the DOM changes — a subtle source of loop bugs. Prefer `querySelectorAll`.

---

## III. READING & CHANGING CONTENT

```js
const el = document.querySelector("#app");

// Text content (safe — treats everything as plain text)
el.textContent = "New text";             // sets text, escapes HTML
const t = el.textContent;                // reads all text inside

// HTML content (powerful but DANGEROUS — see pitfalls)
el.innerHTML = "<strong>Bold</strong>";  // parses as HTML

// Attributes
el.getAttribute("href");
el.setAttribute("href", "/home");
el.removeAttribute("disabled");
el.hasAttribute("href");

// Properties vs attributes (input value, checked, etc.)
const input = document.querySelector("input");
input.value = "typed text";              // property — the live value
input.checked = true;

// data-* attributes via dataset
// <div data-user-id="42" data-role="admin">
el.dataset.userId;     // "42"  (camelCased)
el.dataset.role;       // "admin"
el.dataset.userId = "99";
```

### Styling and classes
```js
// Inline styles (camelCase properties)
el.style.color = "red";
el.style.backgroundColor = "black";
el.style.display = "none";

// Classes — prefer classList over fiddling with className
el.classList.add("active");
el.classList.remove("hidden");
el.classList.toggle("open");         // add if absent, remove if present
el.classList.toggle("open", true);   // force add
el.classList.contains("active");     // true/false
el.classList.replace("old", "new");
```
> ✅ Best practice: put styling in CSS classes and toggle classes from JS, rather than setting many inline `style` properties. It keeps presentation in CSS and logic in JS.

---

## IV. CREATING, INSERTING & REMOVING ELEMENTS

```js
// Create
const li = document.createElement("li");
li.textContent = "New item";
li.classList.add("item");

const list = document.querySelector("ul");

// Insert
list.appendChild(li);              // add as last child
list.prepend(li);                  // add as first child
list.append(li, anotherEl);        // append multiple (and strings)
referenceEl.before(li);            // insert before a sibling
referenceEl.after(li);             // insert after a sibling
list.insertAdjacentHTML("beforeend", "<li>via HTML</li>");

// Remove / replace
li.remove();                       // remove itself
list.removeChild(li);              // older form
oldEl.replaceWith(newEl);
```

### Performance: batch with DocumentFragment
Touching the live DOM repeatedly forces re-layouts. Build off-DOM, then insert once.
```js
const fragment = document.createDocumentFragment();
for (let i = 0; i < 1000; i++) {
  const li = document.createElement("li");
  li.textContent = `Item ${i}`;
  fragment.appendChild(li);          // not in the live DOM yet — cheap
}
list.appendChild(fragment);          // ONE reflow instead of 1000
```

---

## V. EVENTS — RESPONDING TO THE USER

### `addEventListener`
```js
const button = document.querySelector("#save");

button.addEventListener("click", (event) => {
  console.log("clicked!", event);
});

// Named handler so you can remove it later
function onClick(e) { console.log("clicked"); }
button.addEventListener("click", onClick);
button.removeEventListener("click", onClick);  // must be the SAME function reference

// Options
button.addEventListener("click", onClick, { once: true });    // auto-removes after first
button.addEventListener("scroll", onScroll, { passive: true });// perf hint for scroll/touch
```

### The event object
```js
input.addEventListener("input", (e) => {
  e.target;          // the element that fired the event
  e.target.value;    // the input's current value
  e.type;            // "input"
  e.currentTarget;   // the element the listener is attached to
  e.preventDefault();   // stop default behavior (form submit, link nav)
  e.stopPropagation();  // stop the event bubbling further up
});
```

### Common event types
```js
// Mouse
"click", "dblclick", "mousedown", "mouseup", "mousemove", "mouseenter", "mouseleave"
// Keyboard
"keydown", "keyup"        // e.key ("Enter", "a", "ArrowUp"), e.code, e.shiftKey
// Form
"submit", "input", "change", "focus", "blur"
// Window/document
"load", "DOMContentLoaded", "resize", "scroll"
```

### Form handling example
```js
const form = document.querySelector("#login");
form.addEventListener("submit", (e) => {
  e.preventDefault();                  // ⚠️ stop the page from reloading
  const data = new FormData(form);
  const email = data.get("email");
  console.log("submitting", email);
});

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeModal();
  if (e.ctrlKey && e.key === "s") { e.preventDefault(); save(); }
});
```

---

## VI. BUBBLING, CAPTURING & DELEGATION ⭐

### Event flow: capture → target → bubble
When you click an element, the event travels in **three phases**:

```
                  ┌──────────── document ────────────┐
   CAPTURE phase  │   ┌──────── div#parent ───────┐   │  BUBBLE phase
   (top → target) │   │     ┌─── button ───┐       │   │  (target → top)
        │         │   │     │   CLICK HERE  │       │   │       ▲
        ▼         │   │     └───────────────┘       │   │       │
   document ──► div#parent ──► button ──(target)──► div#parent ──► document
```
By default, listeners fire during the **bubble** phase (target outward). The event "bubbles up" through every ancestor.

```js
document.querySelector("#parent").addEventListener("click", () => {
  console.log("parent heard the click");   // fires even if you clicked the button inside
});
document.querySelector("#child").addEventListener("click", () => {
  console.log("child clicked");            // fires first (it's the target)
});
// Click the child → "child clicked" then "parent heard the click"
```

### Capturing phase (rarely needed)
```js
el.addEventListener("click", handler, true);            // capture phase
el.addEventListener("click", handler, { capture: true }); // same
```

### Stopping propagation
```js
child.addEventListener("click", (e) => {
  e.stopPropagation();   // parent's listener will NOT fire now
});
```

### Event delegation ⭐ (the pattern that matters)
Instead of attaching a listener to every child, attach **one** listener to a common parent and use `e.target` to figure out what was clicked. This is efficient and — crucially — works for elements added *after* the listener was set.

```html
<ul id="todo-list">
  <li>Buy milk <button class="delete">x</button></li>
  <li>Walk dog <button class="delete">x</button></li>
  <!-- items may be added dynamically later -->
</ul>
```
```js
// ❌ Naive: a listener per button — breaks for items added later, and is wasteful
document.querySelectorAll(".delete").forEach(btn =>
  btn.addEventListener("click", deleteItem)
);

// ✅ Delegation: ONE listener on the parent
document.querySelector("#todo-list").addEventListener("click", (e) => {
  // Did the click land on (or inside) a delete button?
  const btn = e.target.closest(".delete");
  if (!btn) return;                       // ignore clicks elsewhere
  btn.parentElement.remove();             // remove the whole <li>
});
```
Why delegation wins:
- **One listener** instead of N — less memory, faster setup.
- **Works for future elements** — newly added `<li>`s are handled automatically.
- `e.target.closest(selector)` reliably finds the relevant element even if you clicked a nested child.

> Delegation is how frameworks like React handle events internally — a single root listener that dispatches to the right component.

---

## VII. WAITING FOR THE DOM & SCRIPT TIMING

```js
// Run code only after the HTML is parsed
document.addEventListener("DOMContentLoaded", () => {
  // safe to query elements here
});

// 'load' waits for everything (images, stylesheets) — usually later than you need
window.addEventListener("load", () => { /* all assets ready */ });
```
```html
<!-- Best modern practice: defer the script so the DOM is ready when it runs -->
<script src="app.js" defer></script>
<!-- or place <script> right before </body> -->
```

---

## VIII. COMMON PITFALLS & GOTCHAS

**1. `innerHTML` with user input = XSS vulnerability**
```js
el.innerHTML = userInput;   // ❌ user could inject <script>/<img onerror=...>
el.textContent = userInput; // ✅ safe — rendered as plain text
```

**2. Querying before the DOM exists**
```js
// Script in <head> with no defer:
document.querySelector("#app");  // ❌ null — element not parsed yet
// Fix: defer the script, or wrap in DOMContentLoaded.
```

**3. `removeEventListener` with a different function**
```js
el.addEventListener("click", () => {});  // anonymous — can NEVER be removed
// Use a named function reference for both add and remove.
```

**4. Forgetting `e.preventDefault()` on forms/links** — the page reloads or navigates, wiping your JS state.

**5. Attaching listeners in a loop instead of delegating** — slow, and breaks for dynamic content. Use delegation.

**6. Layout thrashing — reading then writing in a loop**
```js
for (const el of els) {
  el.style.height = el.offsetHeight + 10 + "px"; // ❌ read-then-write forces reflow each time
}
// Batch reads, then batch writes; or use DocumentFragment / requestAnimationFrame.
```

**7. Memory leaks from listeners on removed elements** — remove listeners (or use delegation) when tearing down UI in long-lived apps.

---

## IX. KEY TAKEAWAYS

- The **DOM** is a live tree of node objects the browser builds from HTML; changing it re-renders the page.
- Select with **`querySelector`/`querySelectorAll`** (CSS syntax); `querySelectorAll` is a static snapshot, `getElementsBy*` are live.
- Use **`textContent`** for text (safe) and **`innerHTML`** only with trusted content (XSS risk otherwise).
- Prefer **`classList`** toggles + CSS classes over many inline `style` writes; batch DOM inserts with a **`DocumentFragment`**.
- Handle user actions with **`addEventListener`**; the `event` object gives you `target`, `preventDefault()`, and `stopPropagation()`.
- Events flow **capture → target → bubble**; listeners fire on bubble by default.
- **Event delegation ⭐** — one listener on a parent + `e.target.closest()` — is efficient and handles dynamically added elements. It's the pattern to reach for.
- Run DOM code after **`DOMContentLoaded`** or use `<script defer>`.

---

**← Prev:** [`06-ES6-Plus-Features.md`](./06-ES6-Plus-Features.md) | **→ Next:** [`08-Advanced-JS-Patterns.md`](./08-Advanced-JS-Patterns.md) | **Index:** [`00-Index.md`](./00-Index.md)
