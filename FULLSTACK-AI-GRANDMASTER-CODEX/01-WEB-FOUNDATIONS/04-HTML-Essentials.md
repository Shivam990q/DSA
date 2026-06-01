# 📄 HTML Essentials

> *"HTML is the skeleton of every web page. Write it well — semantically, accessibly — and everything you layer on top (CSS, JS, React) is cleaner."*

HTML (HyperText Markup Language) describes the **structure and content** of a page. It is not a programming language — there's no logic, no loops — it's a *markup* language: you tag content to give it meaning. This chapter teaches you to write HTML the way professionals do: **semantic, accessible, and well-structured**, not a soup of `<div>`s.

---

## I. THE ANATOMY OF AN HTML DOCUMENT

Every HTML page follows this skeleton. Type it out and understand each line:

```html
<!DOCTYPE html>                          <!-- Tells the browser: this is modern HTML5 -->
<html lang="en">                         <!-- Root element; lang aids screen readers & SEO -->
  <head>                                 <!-- Metadata: NOT shown on the page -->
    <meta charset="UTF-8" />             <!-- Character encoding (use UTF-8 always) -->
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0" />  <!-- Essential for responsive/mobile -->
    <title>My Page</title>               <!-- Shown in the browser tab; vital for SEO -->
    <meta name="description"
          content="A short summary for search engines." />
    <link rel="stylesheet" href="styles.css" />   <!-- External CSS -->
  </head>
  <body>                                 <!-- Everything VISIBLE goes here -->
    <h1>Hello, world</h1>
    <p>This is a paragraph.</p>
    <script src="app.js" defer></script> <!-- JS, deferred so it doesn't block parsing -->
  </body>
</html>
```

### Anatomy of a tag
```
       opening tag        attributes          closing tag
          │                  │                    │
        <a   href="/about"  class="nav-link" >  About  </a>
                                                  │
                                              content
```
- **Elements** = opening tag + content + closing tag. Some are **void/self-closing** (no content): `<img>`, `<br>`, `<input>`, `<meta>`.
- **Attributes** configure an element: `href`, `src`, `class`, `id`, `alt`, etc. They go in the opening tag as `name="value"`.

> **The `<meta name="viewport">` tag is not optional.** Without it, mobile browsers render the page at desktop width and shrink it, breaking responsive design. Every page needs it.

---

## II. SEMANTIC HTML — TAGS WITH MEANING

The single biggest difference between amateur and professional HTML is **semantics**: choosing tags that describe *what content is*, not just how it looks. A `<div>` means nothing; a `<nav>` means "this is navigation."

### Why semantics matter
1. **Accessibility** — screen readers use semantics to let blind users navigate ("jump to main content," "list the headings").
2. **SEO** — search engines understand structured content better and rank it accordingly.
3. **Maintainability** — `<article>` is self-documenting; `<div class="article">` is a guess.
4. **Default behavior** — `<button>` is keyboard-focusable and clickable by default; a `<div>` styled as a button is none of those without extra work.

### The semantic layout elements

```html
<body>
  <header>            <!-- Site/page header: logo, top nav -->
    <nav>             <!-- Navigation links -->
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/blog">Blog</a></li>
      </ul>
    </nav>
  </header>

  <main>              <!-- THE main content. Only ONE per page. -->
    <article>         <!-- Self-contained content (a blog post, a news story) -->
      <h1>Article Title</h1>
      <section>       <!-- A thematic grouping within the article -->
        <h2>Introduction</h2>
        <p>...</p>
      </section>
    </article>

    <aside>           <!-- Tangentially related content: sidebar, related links -->
      <h2>Related</h2>
    </aside>
  </main>

  <footer>            <!-- Footer: copyright, contact, secondary nav -->
    <p>&copy; 2024 My Site</p>
  </footer>
</body>
```

### Semantic vs non-semantic — the contrast

```html
<!-- ❌ "div soup": no meaning, bad for accessibility & SEO -->
<div class="header">
  <div class="nav">
    <div class="nav-item" onclick="go()">Home</div>
  </div>
</div>

<!-- ✅ Semantic: meaning is built in, accessible & SEO-friendly by default -->
<header>
  <nav>
    <a href="/">Home</a>
  </nav>
</header>
```

### Common semantic/text elements

| Element | Meaning |
|---|---|
| `<h1>`–`<h6>` | Headings, in order of importance. **One `<h1>` per page.** Don't skip levels. |
| `<p>` | Paragraph |
| `<a href>` | Anchor / hyperlink |
| `<ul>` / `<ol>` / `<li>` | Unordered / ordered lists and items |
| `<strong>` / `<em>` | Important / emphasized text (semantic, vs `<b>`/`<i>` which are visual only) |
| `<figure>` / `<figcaption>` | An image/diagram with a caption |
| `<time datetime="...">` | A machine-readable date/time |
| `<button>` | An interactive button (use this, not a clickable div!) |
| `<table>`, `<thead>`, `<tbody>`, `<tr>`, `<th>`, `<td>` | Tabular data (not for layout!) |

> **Gotcha — headings are an outline, not font sizes.** Use `<h1>`→`<h6>` to convey *document structure*, not to make text big. If you want big text that isn't a heading, use CSS. Screen-reader users navigate by heading hierarchy; skipping from `<h1>` to `<h4>` breaks that outline.

---

## III. LINKS AND IMAGES

```html
<!-- Links -->
<a href="https://example.com">External link</a>
<a href="/about">Internal link (relative path)</a>
<a href="#section-2">Jump to an element with id="section-2"</a>
<a href="mailto:hi@example.com">Email link</a>
<!-- Opening in a new tab? Add rel="noopener" for security (prevents tabnabbing): -->
<a href="https://example.com" target="_blank" rel="noopener noreferrer">New tab</a>

<!-- Images: ALWAYS include alt text -->
<img src="/cat.jpg" alt="A ginger cat sleeping on a keyboard" width="400" height="300" />
<!-- alt="" (empty) for purely decorative images, so screen readers skip them -->
<img src="/divider.png" alt="" />
```

> **`alt` text is mandatory, not optional.** It's read aloud to blind users, shown when the image fails to load, and indexed by search engines. Describe the image's *purpose*. Decorative images get `alt=""` (empty) so assistive tech skips them. Also: setting `width`/`height` reserves space and prevents layout shift (see CLS in the performance chapter).

---

## IV. FORMS — HOW USERS SEND DATA

Forms are how users submit data to your backend. Getting them right (and accessible) is a core skill.

```html
<form action="/signup" method="POST">
  <!-- Every input needs a <label>. The "for" attribute links it to the input's "id". -->
  <div>
    <label for="email">Email address</label>
    <input
      type="email"            <!-- type drives validation + mobile keyboard -->
      id="email"
      name="email"            <!-- "name" is the key sent to the server -->
      placeholder="you@example.com"
      required                <!-- built-in HTML validation -->
      autocomplete="email"
    />
  </div>

  <div>
    <label for="password">Password</label>
    <input type="password" id="password" name="password"
           minlength="8" required />
  </div>

  <div>
    <label for="role">Role</label>
    <select id="role" name="role">
      <option value="dev">Developer</option>
      <option value="design">Designer</option>
    </select>
  </div>

  <fieldset>
    <legend>Notifications</legend>     <!-- groups related controls, announced by screen readers -->
    <label><input type="checkbox" name="news" /> Email me news</label>
    <label><input type="radio" name="plan" value="free" /> Free</label>
    <label><input type="radio" name="plan" value="pro" /> Pro</label>
  </fieldset>

  <div>
    <label for="bio">Bio</label>
    <textarea id="bio" name="bio" rows="4"></textarea>
  </div>

  <button type="submit">Sign up</button>
</form>
```

### Input types matter
Using the right `type` gives you free validation and the right mobile keyboard:

| `type` | Use for | Bonus |
|---|---|---|
| `text` | General text | — |
| `email` | Email | Validates format; email keyboard on mobile |
| `password` | Passwords | Masks input |
| `number` | Numbers | Numeric keypad; min/max/step |
| `tel` | Phone | Phone keypad on mobile |
| `url` | Web addresses | Validates URL format |
| `date` / `time` | Dates/times | Native date picker |
| `checkbox` / `radio` | Multiple / single choice | — |
| `file` | File uploads | — |

### The label–input connection (critical for accessibility)
```html
<!-- ✅ Linked: clicking the label focuses the input; screen readers announce it -->
<label for="username">Username</label>
<input id="username" name="username" />

<!-- ✅ Also valid: wrapping the input inside the label -->
<label>Username <input name="username" /></label>

<!-- ❌ Broken: label not associated with any input -->
<label>Username</label>
<input name="username" />
```

> **Gotcha — client-side validation is a convenience, never a security boundary.** `required`, `minlength`, `type="email"` improve UX, but anyone can bypass the form entirely with curl/Postman. **The server must always re-validate.** (See `02-HTTP-And-HTTPS.md` §XI and `06-...Security-Basics.md`.)

---

## V. ACCESSIBILITY (a11y) ESSENTIALS

Accessibility means people with disabilities (visual, motor, cognitive) can use your site. It's a legal requirement in many places, it overlaps heavily with SEO, and it's simply the right thing to do. Most of it is free if you write semantic HTML.

### The core rules
1. **Use semantic elements.** `<button>`, `<nav>`, `<main>`, headings — they carry built-in accessibility.
2. **Every image has `alt`.** Descriptive for meaningful images, empty for decorative.
3. **Every form control has a `<label>`.**
4. **Keyboard navigation works.** Users who can't use a mouse must reach everything with Tab/Enter/Space. Semantic elements get this for free; custom `<div>` widgets don't.
5. **Sufficient color contrast** between text and background (a CSS concern, but plan for it).
6. **Logical heading order** (`h1` → `h2` → `h3`, no skips) — it's the screen-reader table of contents.

### ARIA — for when HTML isn't enough
**ARIA** (Accessible Rich Internet Applications) attributes add accessibility info that HTML alone can't express — but the first rule of ARIA is **"don't use ARIA if a native element does the job."**

```html
<!-- Use a real button (accessible by default) ... -->
<button>Menu</button>

<!-- ...not a div that needs ARIA + JS to fake what <button> gives free: -->
<div role="button" tabindex="0"
     aria-pressed="false"
     onkeydown="/* handle Enter & Space manually */">Menu</div>

<!-- Legitimate ARIA: labeling an icon-only button that has no visible text -->
<button aria-label="Close dialog">✕</button>

<!-- Announcing dynamic updates to screen readers -->
<div aria-live="polite" id="status"></div>  <!-- JS updates this; SR reads it aloud -->
```

| Common ARIA attribute | Purpose |
|---|---|
| `aria-label` | Gives an accessible name (for icon-only controls) |
| `aria-labelledby` | Points to another element that labels this one |
| `aria-describedby` | Points to extra descriptive text |
| `aria-live` | Announces dynamic content changes |
| `aria-hidden="true"` | Hides decorative content from screen readers |
| `role` | Declares what an element *is* (use sparingly; prefer native tags) |

> **Test it yourself:** Try navigating your page with the **Tab key only** — no mouse. Can you reach and activate everything? Run a browser audit (Chrome DevTools → Lighthouse → Accessibility). Note: automated tools catch only part of the picture; full WCAG compliance requires manual testing with real assistive technologies and expert review.

---

## VI. A COMPLETE, ACCESSIBLE PAGE EXAMPLE

Putting it together — a small but professionally-structured page:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Ada Lovelace — Profile</title>
    <meta name="description" content="A short profile of Ada Lovelace." />
  </head>
  <body>
    <header>
      <nav aria-label="Primary">
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/about">About</a></li>
        </ul>
      </nav>
    </header>

    <main>
      <article>
        <h1>Ada Lovelace</h1>
        <p>Published <time datetime="2024-01-15">January 15, 2024</time></p>

        <figure>
          <img src="/ada.jpg" alt="Portrait of Ada Lovelace" width="300" height="400" />
          <figcaption>Ada Lovelace, the first programmer.</figcaption>
        </figure>

        <section>
          <h2>Early life</h2>
          <p>She was the daughter of Lord Byron...</p>
        </section>

        <section>
          <h2>Contributions</h2>
          <p>She wrote the first <strong>algorithm</strong> intended for a machine.</p>
        </section>
      </article>

      <aside>
        <h2>See also</h2>
        <ul>
          <li><a href="/charles-babbage">Charles Babbage</a></li>
        </ul>
      </aside>
    </main>

    <footer>
      <p>&copy; 2024 History of Computing</p>
    </footer>
  </body>
</html>
```

---

## VII. COMMON PITFALLS / GOTCHAS

- **`<div>` soup** — wrapping everything in `<div>`s. Reach for `<header>`, `<main>`, `<nav>`, `<article>`, `<section>`, `<button>` first.
- **Clickable `<div>`s instead of `<button>`/`<a>`** — they aren't keyboard-focusable or screen-reader-announced without manual ARIA + JS. Use the real element.
- **Missing `alt` attributes** — breaks accessibility and SEO. Always include one (empty for decorative).
- **Missing the viewport `<meta>`** — your responsive CSS won't work on mobile.
- **Unlabeled form inputs** — `<label for>`/`id` pairs are mandatory for accessibility.
- **Skipping heading levels** (`h1` → `h4`) — breaks the document outline screen readers rely on.
- **Trusting HTML5 form validation for security** — it's UX only; the server must re-validate.
- **Multiple `<h1>` or `<main>`** — there should be one main heading and one `<main>` per page.
- **Using tables for layout** — tables are for tabular *data*; use CSS grid/flexbox for layout.

---

## ✅ KEY TAKEAWAYS

- HTML is a **markup** language describing **structure and content** — every page starts with `<!DOCTYPE html>`, `<html lang>`, `<head>` (metadata), and `<body>` (visible content).
- **Semantic elements** (`<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>`, `<button>`) carry meaning that powers **accessibility, SEO, and maintainability** — prefer them over `<div>` soup.
- The **viewport meta tag** and **UTF-8 charset** are mandatory on every page.
- **Images need `alt`**; **form inputs need `<label>`s**; **headings** form an ordered outline (one `<h1>`, no skips).
- Forms send data with the right input **`type`** for free validation + correct mobile keyboards — but client validation is UX only; the **server must always re-validate**.
- **Accessibility is mostly free** with semantic HTML; use **ARIA only when native elements can't express something**, and test with keyboard-only navigation plus audits (knowing automated tools are not full WCAG validation).

---

**→ Next:** [`05-CSS-Essentials.md`](./05-CSS-Essentials.md) — styling and laying out the structure you just built
**← Prev:** [`03-Browsers-And-Rendering.md`](./03-Browsers-And-Rendering.md)
**🗺️ Index:** [`00-Index.md`](./00-Index.md)
