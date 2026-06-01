# 🌐 Web Foundations

> *"Master this layer and you can debug anything above it. Skip it and you'll be confused forever."*

This is the bedrock of the entire codex. Everything — React, Next.js, Node, deployment, even AI apps — is built on top of how the internet, HTTP, and browsers actually work. The hours you invest here pay off in every section that follows.

---

## 📚 Contents (learning order)

| # | File | What you'll learn |
|---|---|---|
| 0 | [`00-Index.md`](./00-Index.md) | This page — the map |
| 1 | [`01-How-The-Internet-Works.md`](./01-How-The-Internet-Works.md) | DNS, IP, TCP/IP, packets, ISPs — how a URL becomes a page |
| 2 | [`02-HTTP-And-HTTPS.md`](./02-HTTP-And-HTTPS.md) | Requests/responses, methods, status codes, headers, cookies, TLS |
| 3 | [`03-Browsers-And-Rendering.md`](./03-Browsers-And-Rendering.md) | DOM, CSSOM, render tree, reflow/repaint, the event loop |
| 4 | [`04-HTML-Essentials.md`](./04-HTML-Essentials.md) | Semantic HTML, forms, accessibility, document structure |
| 5 | [`05-CSS-Essentials.md`](./05-CSS-Essentials.md) | Selectors, box model, flexbox, grid, responsive design, specificity |
| 6 | [`06-Web-Performance-And-Security-Basics.md`](./06-Web-Performance-And-Security-Basics.md) | Caching, CDN, lazy loading; XSS, CSRF, CORS, HTTPS |

---

## 🧭 WHY THIS ORDER

```
01 Internet      →  the network: how bytes travel between machines
02 HTTP/HTTPS    →  the language those machines speak over that network
03 Browsers      →  what the client does with the bytes it receives
04 HTML          →  the structure/content the browser parses
05 CSS           →  the styling layered onto that structure
06 Perf/Security →  doing all of the above fast and safely
```

We go **bottom-up**: network → protocol → client → content → style → quality. Each file assumes the one before it. By the end you'll be able to picture the full journey from a keystroke to a rendered, styled, secure page.

---

## 🎯 WHAT YOU'LL BE ABLE TO DO

After this section you can:
- Explain, end to end, what happens when someone visits a URL.
- Read and reason about HTTP requests/responses, status codes, and headers.
- Hand-write clean, **semantic, accessible** HTML.
- Build **responsive** layouts with flexbox and grid, and reason about CSS specificity.
- Understand the browser's rendering pipeline and why some operations are slow.
- Recognize and prevent the most common web vulnerabilities (XSS, CSRF, CORS misconfig).

These are the prerequisites for `02-JAVASCRIPT-MASTERY` and everything after.

---

## 🛠️ HOW TO STUDY THIS SECTION

1. **Read with the browser DevTools open.** Press F12, watch the Network tab as pages load, inspect elements in the Elements tab. Theory + observation = understanding.
2. **Type the code, don't copy it.** Every code block here is meant to be run. Make a scratch `.html` file and experiment.
3. **Break things on purpose.** Send a bad request, write invalid HTML, over-specify a CSS selector — watch what happens.
4. **Build the section project:** a responsive, accessible, multi-page static site (no framework). That's your build gate before JavaScript.

---

**→ Start:** [`01-How-The-Internet-Works.md`](./01-How-The-Internet-Works.md)
**🏠 Codex root:** [`../README.md`](../README.md)
**🗺️ Roadmap:** [`../00-ROADMAP-AND-PHILOSOPHY/00-Index.md`](../00-ROADMAP-AND-PHILOSOPHY/00-Index.md)
